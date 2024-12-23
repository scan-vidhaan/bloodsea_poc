step 1:def read_csv()
step 2: find columns 
[
Have you donated platelets
Number of donations
Are you under any medical condition
Will you donate blood if you stay close to needy.
Do you Smoke
Do you Drink
Will you donate blood during an emergency ?
  Have you participated in any blood donation campaigns before?  
Do you feel comfortable donating blood? 
Are you donating blood for activity points ?
Have you donated blood during an emergency ?
Imtent score
]
step 3 : assign  weights to the value based on  
    [
Have you donated platelets yes/no
Number of donations higher number of donations more the weight ignore non numeric values in the feild 
Are you under any medical condition  yes or no 
Will you donate blood if you stay close to needy. yes or no 
Do you Smoke yes or no 
Do you Drink  Ocationally or Regularly or I do not Drink 
Will you donate blood during an emergency ? yes or no 
  Have you participated in any blood donation campaigns before?  yes or no
Do you feel comfortable donating blood? Very Comfortable or Comfortable or Nutral or Not Comfortable
Are you donating blood for activity points ? yes or no 
Have you donated blood during an emergency ? yesor no 
Intent Score highest intent moreweight range is 0-23 
]
 step 4 
 add all the weight for each row create a column in the existing csv named Behaviour analysis
 step 5
 and sort the csv based on the blood group and behaviour analysis in decending order 




