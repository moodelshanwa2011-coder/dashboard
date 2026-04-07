<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>KPI Dashboard</title>

<style>

body{
    font-family: Arial, sans-serif;
    background:#f4f6f8;
    text-align:center;
}

/* ===== Title ===== */
.main-title{
    font-size:28px;
    font-weight:bold;
    margin:30px 0;
}

/* ===== Container ===== */
.kpi-container{
    display:flex;
    justify-content:center;
    gap:25px;
    flex-wrap:wrap;
}

/* ===== Box ===== */
.kpi-box{
    background:white;
    padding:20px;
    border-radius:12px;
    width:140px;
    box-shadow:0 4px 10px rgba(0,0,0,0.1);
}

/* ===== Name ===== */
.kpi-name{
    font-size:18px;
    margin-bottom:15px;
    font-weight:bold;
}

/* ===== Circle ===== */
.circle{
    width:80px;
    height:80px;
    border-radius:50%;
    border:6px solid #2c7be5;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:18px;
    font-weight:bold;
    margin:auto;
    color:#2c7be5;
}

</style>
</head>

<body>

<div class="main-title">Patient Safety Indicators</div>

<div class="kpi-container">

    <div class="kpi-box">
        <div class="kpi-name">Injury</div>
        <div class="circle">0.01</div>
    </div>

    <div class="kpi-box">
        <div class="kpi-name">Pressure</div>
        <div class="circle">9.54</div>
    </div>

    <div class="kpi-box">
        <div class="kpi-name">CLABSI</div>
        <div class="circle">1.8</div>
    </div>

    <div class="kpi-box">
        <div class="kpi-name">VAE</div>
        <div class="circle">1.1</div>
    </div>

    <div class="kpi-box">
        <div class="kpi-name">CAUTI</div>
        <div class="circle">1.13</div>
    </div>

</div>

</body>
</html>
