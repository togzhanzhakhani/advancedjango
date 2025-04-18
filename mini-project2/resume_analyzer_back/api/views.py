import docx
import PyPDF2
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Specialization, Skill, Resume
from .serializers import SpecializationSerializer, RegisterSerializer, ResumeSerializer
from django.contrib.auth.models import Group, User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
import spacy
from .utils import analyze
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView

@api_view(['POST'])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        role = request.data.get("role")
        if role == "job_seeker":
            group = Group.objects.get(name="Job Seeker")
        elif role == "recruiter":
            group = Group.objects.get(name="Recruiter")
        else:
            return Response({'message': 'Invalid role'}, status=400)
        user.groups.add(group)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(str(user.pk).encode())
        conf_link = f'http://localhost:3000/confirm-email/{uid}/{token}/'
        mail_subject = 'Confirm your email address'
        message = f"Please confirm your email by clicking the following link: {conf_link}/"
        send_mail(mail_subject, message, 'admin@example.com', [user.email])
        return Response({'message': 'User registered successfully!'}, status=201)    
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def confirm_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return Response({"message": "Email confirmed successfully!"})
    return Response({"message": "Invalid or expired token."}, status=400)

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = response.data.get('access')
        access_token = AccessToken(token)
        user = User.objects.get(id=access_token['user_id'])
        role = "job_seeker"  
        if user.groups.filter(name="Job Seeker").exists():
            role = "job_seeker"
        elif user.groups.filter(name="Recruiter").exists():
            role = "recruiter"
        response_data = response.data
        response_data['role'] = role 
        return Response(response_data)

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def analyze_resume(text, specialization_id):
    skills = Skill.objects.filter(specialization_id=specialization_id)
    skills_list = [skill.name.lower() for skill in skills]
    nlp = spacy.load("en_core_web_sm")
    results = nlp(text)
    return analyze(skills_list, text, results)

@api_view(['POST'])
def upload_resume(request):
    if request.method == 'POST':
        file = request.FILES['file']
        specialization_id = request.data.get('specialization')
        if file.name.endswith('.pdf'):
            resume_text = extract_text_from_pdf(file)
        elif file.name.endswith('.docx'):
            resume_text = extract_text_from_docx(file)
        else:
            return Response({"error": "Invalid file type"}, status=400)
        result = analyze_resume(resume_text, specialization_id)
        resume = Resume.objects.create(user=request.user, specialization_id=specialization_id, file=file)
        return Response({"message": "Resume uploaded and analyzed successfully", "data": result}, status=201)
    
@api_view(['GET'])
def get_specializations(request):
    specializations = Specialization.objects.all()
    serializer = SpecializationSerializer(specializations, many=True)
    return Response(serializer.data)

class ResumeListView(APIView):
    def get(self, request):
        resumes = Resume.objects.all()
        serializer = ResumeSerializer(resumes, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def password_reset_request(request):
    email = request.data.get('email')
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"message": "Email does not exist in our records."}, status=400)
    uid = urlsafe_base64_encode(str(user.pk).encode())
    token = default_token_generator.make_token(user)
    reset_link = f'http://localhost:3000/new-password/{uid}/{token}/'
    mail_subject = 'Reset your password'
    message = f"Click the following link to reset your password: {reset_link}"
    send_mail(mail_subject, message, 'admin@example.com', [user.email])
    return Response({"message": "Password reset link sent to email!"}, status=200)

@api_view(['POST'])
def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, User.DoesNotExist):
        return Response({"message": "Invalid link."}, status=400)
    if default_token_generator.check_token(user, token):
        new_password = request.data.get('new_password')
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password reset successfully!"}, status=200)
    else:
        return Response({"message": "Invalid or expired token."}, status=400)