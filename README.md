# Steps to run locally
Make sure you have python3 and virtualenv installed 
step 1 
```
git clone https://github.com/saty-git24/pdf-sum.git
```
step 2
```
cd pdf-sum
```
step 3
```
python3 -m venv venv
```
step 4
```
source venv/bin/activate
```
step 5
```
pip install -r requirements.txt
```
step 6
```
npm install
```
step 7
```
Setup up your environment variables using sample.env in .env.local
```
step 8
```
npx convex dev
```
step 9 <br>
Then in new terminal run
```
python3 run.py
```
<br>
Your flask server will be up and running in sync with convex database :)
