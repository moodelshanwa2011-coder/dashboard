<!DOCTYPE html>
<html lang="ar">
<head>
<meta charset="UTF-8">
<style>

body{
    font-family: Arial;
    text-align:center;
}

/* اخفاء الجدول */
table{
    display:none;
}

/* شكل الدوائر */
.circle{
    width:100px;
    height:100px;
    border-radius:50%;
    background:#4CAF50;
    color:white;
    display:inline-flex;
    justify-content:center;
    align-items:center;
    font-size:22px;
    margin:10px;
}

</style>
</head>
<body>

<h2 id="monthName"></h2>

<div id="circles"></div>

<script>

const months = [
    {name:"يناير", values:[10,20,30]},
    {name:"فبراير", values:[15,25,35]},
    {name:"مارس", values:[12,22,32]},
    {name:"ابريل", values:[18,28,38]}
];

let index = 0;

function showMonth(){
    const month = months[index];

    document.getElementById("monthName").innerText = month.name;

    let html = "";
    month.values.forEach(num=>{
        html += `<div class="circle">${num}</div>`;
    });

    document.getElementById("circles").innerHTML = html;

    index++;
    if(index >= months.length){
        index = 0;
    }
}

/* عرض أول شهر */
showMonth();

/* تغيير كل 10 ثواني */
setInterval(showMonth, 10000);

</script>

</body>
</html>
