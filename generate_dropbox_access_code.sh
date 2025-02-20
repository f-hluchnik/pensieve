#/bin/bash
echo -n "Enter APP_KEY:" 
read -r APP_KEY

echo -n "Enter APP_SECRET:" 
read -r APP_SECRET
BASIC_AUTH=$(printf "%s:%s" "$APP_KEY" "$APP_SECRET" | base64 -b 0)


echo "Navigate to URL and get ACCESS CODE"
echo "https://www.dropbox.com/oauth2/authorize?client_id=$APP_KEY&token_access_type=offline&response_type=code"

echo -n "Return to this script once you have the ACCESS_CODE. Press Enter to continue." 
read DUMMY

echo -n "Enter the ACCESS_CODE:" 
read -r ACCESS_CODE_GENERATED

curl --location "https://api.dropboxapi.com/oauth2/token" \
--header "Content-Type: application/x-www-form-urlencoded" \
--header "Authorization: Basic $BASIC_AUTH" \
--data-urlencode "code=$ACCESS_CODE_GENERATED" \
--data-urlencode "grant_type=authorization_code"

