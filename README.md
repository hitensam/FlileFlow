# File Flow Application

### Setup

1. **Virtual Environment:**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

### Database & Server

1. **Database Setup:**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

2. **Run the Server:**
   ```bash
   python manage.py runserver
   ```

3. **Access:**
   - Application: [http://localhost:8000/](http://localhost:8000/)
   - Admin Panel: [http://localhost:8000/admin/](http://localhost:8000/admin/)

### Usage

Share files from ops user to client user.

### Deactivate Environment

```bash
deactivate
```

For any questions, reach out!

Exported data from Postman: **dump_v21**

**Enter your email id credential to get OTP. in SendOTP.py**

**SAMPLE OTP EMAIL** <br>
![image](https://github.com/hitensam/FlileFlow/assets/30778907/a0f027f7-f80f-4f74-a04e-7e45ce9df8d9)
