# The solution for problem "Acme Order DB"

## TL;DR
Bypass the login by altering the session then perform LDAP injection to bypass filtering.

## Solution:
1. First thing we noticed is that there is a login page. We tried to log in but of course we have no credentials, so we fail.
![The front page](Unknown)
2. We fire up BurpSuite and intercept the request. We notice as sess value that looks like it's base64 encoded.
![The Burp Suite page](Unknown-3)
3. We switch to the decoder tab, decode it and it's username==admin::logged_in=false. So let's try to change that value, encode it back and resend the request.
![The decoder page](Unknown-2)
4. Good, we logged in! Now we are greeted with a search bar and a filter button, we try pressing it and results show up, after a few tries it looks like an ldap query. We check the source file and it's mentioned there so we are on the right track!
![The source page](Unknown-4)
5. We notice that the Coyote files have a weird randomly looking string as a directory, we try going there and fail. Maybe the flag is in another random directory?
6. Lets try some LDAP injections, we notice that the query looks like it's being filtered with an & operator.
7. We mess around with different attributes we figure out 'ou' is used for the classification!. 
8. We can't do much which the already existing & filter so we try injection a second filter using the | operator. It works!
![The page with LDAP files](Unknown-5)
9. we flag path and we have the flag!
