#!/bin/bash

bold=$(tput bold)
green="\033[0;32m"
red='\033[0;31m'
normal=$(tput sgr0)

echo -ne "${green}What is your unique bundle ID that will last forever for this app (i.e. com.yourname.YourApp): ${normal}"
read bundle_id
periods=`echo $bundle_id | grep -o "\." | wc -l`

if [ $periods -ne 2 ]
  then
    echo "${red}You must specify a reverse-domain notation bundle ID for your apps.${normal}"
    echo
    exit -1
fi

echo "${bold}Okay, we'll call it $bundle_id.${normal}"
echo

echo -n "Email address: "
read user
echo -n "Password: "
read -s password


echo
echo "COPY FILES TO A NEW DIRECTORY"
echo "Creating directory ../$bundle_id"
mkdir ../$bundle_id

echo "Copying all the files from this lesson into ../$bundle_id"
cp * ../$bundle_id/
cd ..

echo
echo "CREATE A NEW APP IN YOUR ACCOUNT"
echo "${bold}composer --new $bundle_id${normal}"
./composer --new $bundle_id -u $user -p $password

echo
echo "COMMIT YOUR APP"
echo "${bold}composer --commit $bundle_id${normal}"
./composer --commit $bundle_id -u $user -p $password

echo
echo "PURCHASE YOUR APP"
echo "${bold}composer --purchase $bundle_id${normal}"
./composer --purchase $bundle_id -u $user -p $password

echo
echo "RUN YOUR APP LOCALLY"
echo "Refer to the 'version.json' and 'app.py' files to identify what inputs trigger this app to execute"
echo "${bold}composer --run $bundle_id${normal}"
./composer --run $bundle_id -u $user -p $password
