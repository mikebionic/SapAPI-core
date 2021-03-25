var rateValue = 3.6;

roundedRate = Math.round(rateValue*2)/2

qty = parseInt(roundedRate);          
afterDot = roundedRate - qty

if (afterDot > 0){
    sumValues = qty+1;
}

for (var i=0; i<qty; i++){
    console.log('star');
}
if (afterDot>0){
    console.log('start-half-o');
}
for (var i=0; i<(5-sumValues);i++){
    console.log('start-o');
}