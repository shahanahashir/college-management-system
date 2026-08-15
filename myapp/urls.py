from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [
    path('',views.logins),
    path('logins_post',views.logins_post),
    path('logouts',views.logouts),


    #----------------------------------------- admin-----------------------------------------------------------------------
    path('admin_dashboard',views.admin_dashboard),

    path('add_department',views.add_department),
    path('add_department_post',views.add_department_post),
    path('manage_department',views.manage_department),
    path('edit_department/<id>',views.edit_department),
    path('edit_department_post',views.edit_department_post),
    path('delete_department/<id>', views.delete_department),

    path('add_course/<id>',views.add_course),
    path('add_course_post',views.add_course_post),
    path('manage_course/<id>',views.manage_course),
    path('edit_course/<id>',views.edit_course),
    path('edit_course_post',views.edit_course_post),
    path('delete_course/<id>', views.delete_course),

    path('add_staff/<id>', views.add_staff),
    path('add_staff_post',views.add_staff_post),
    path('manage_staff/<id>',views.manage_staff),
    path('edit_staff/<id>',views.edit_staff),
    path('edit_staff_post',views.edit_staff_post),
    path('delete_staff/<id>',views.delete_staff),

    path('add_hod/<id>',views.add_hod),
    path('view_hod/<id>',views.view_hod),
    path('setting_hod/<id>',views.setting_hod),
    path('remove_hod/<id>',views.remove_hod),
    path('setting_hod_post',views.setting_hod_post),

    path('view_feedback',views.view_feedback),
    path('send_reply/<id>',views.send_reply),
    path('send_reply_post',views.send_reply_post),

    path('add_notification',views.add_notification),
    path('add_notification_post',views.add_notification_post),
    path('manage_notification',views.manage_notification),
    path('edit_notification/<id>',views.edit_notification),
    path('edit_notification_post',views.edit_notification_post),
    path('delete_notification/<id>',views.delete_notification),
    path('view_payment/<id>',views.view_payment),
    path('admin_change_password',views.admin_change_password),
    path('admin_change_password_post',views.admin_change_password_post),

    # ----------------------------------------------------hod-----------------------------------------------------------------

    path('hod_dashboard',views.hod_dashboard),
    path('view_course',views.view_course),

    # -------------------student----------------------
    path('add_student', views.add_student),
    path('add_student_post', views.add_student_post),
    path('manage_student', views.manage_student),
    path('edit_student/<id>', views.edit_student),
    path('edit_student_post', views.edit_student_post),
    path('delete_student/<id>', views.delete_student),

    # -------------------------subject-------------------------
    path('add_subject', views.add_subject),
    path('add_subject_post', views.add_subject_post),
    path('manage_subject', views.manage_subject),
    path('edit_subject/<id>', views.edit_subject),
    path('edit_subject_post', views.edit_subject_post),
    path('delete_subject/<id>', views.delete_subject),
    path('allocate_staff/<id>', views.allocate_staff),
    path('allocate_staff_post', views.allocate_staff_post),
    path('allocated_staff_subject', views.allocated_staff_subject),

    # ===================chat to student---------------------------
    path('chatt/<u>',views.chatt),
    path('chatsnd',views.chatsnd),
    path('chatrply',views.chatrply),

    # ===================change password---------------------------
    path('hod_change_password',views.hod_change_password),
    path('hod_change_password_post',views.hod_change_password_post),

    # -----------------------------------view profile------------
    path('my_profile',views.my_profile),

    #-------------------------------------------- forgot password=============================================================
    path('forgotpassword', views.forgotpassword),
    path('forgotpasswordbuttonclick', views.forgotpasswordbuttonclick),
    path('otp', views.otp),
    path('otpbuttonclick', views.otpbuttonclick),
    path('forgotpswdpswed', views.forgotpswdpswed),
    path('forgotpswdpswedbuttonclick', views.forgotpswdpswedbuttonclick),

# ============================================student app=======================================================================

    path('logins_flutter', views.logins_flutter),
    path('change_password_flutter', views.change_password_flutter),
    path('student_profile_flutter', views.student_profile_flutter),
    path('view_course_info_flutter', views.view_course_info_flutter),
    path('view_subject_flutter', views.view_subject_flutter),
    path('view_hod_flutter', views.view_hod_flutter),
    path('chat_flutter', views.chat_flutter),
    path('view_notification_flutter', views.view_notification_flutter),
    path('payment_histoy_flutter', views.payment_histoy_flutter),
    path('make_payment_flutter', views.make_payment_flutter),
    path('send_feedback_flutter', views.send_feedback_flutter),
    path('view_feedback_flutter', views.view_feedback_flutter),


    path('forgotemail', views.forgotemail),
    path('forgotpass', views.forgotpass),

    # -----------chat flutter------------------
    path('user_sendchat', views.user_sendchat),
    path('user_viewchat', views.user_viewchat),

    # ----------------------payment flutter--------------
    path('payment_flutter', views.payment_flutter),


]
urlpatterns+=static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)