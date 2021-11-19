
# To use mail account for server management
**configure less secure apps if email is not sending**
https://www.google.com/settings/security/lesssecureapps

----------

If you get the errors of 

try to login your account and accept unlock captcha:
https://accounts.google.com/DisplayUnlockCaptcha

----------

If you still cannot connect, try to check connection with the shell command:

```bash
telnet smtp.googlemail.com 587
```
You should see **connected** message

----------

If it still didn't work try to read google docs

https://support.google.com/accounts/answer/185833

----------

if you use 2 factor auth, then create APP PASSWORD