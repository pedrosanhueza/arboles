import streamlit as st
import streamlit.components.v1 as components

# bootstrap 4 collapse example
components.html(
    """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Excel File Upload Example</title>
</head>
<body>

    <h1>Excel File Upload Form</h1>

    <form action="/upload" method="post" enctype="multipart/form-data">
        <label for="excelFile">Choose an Excel file:</label>
        <input type="file" id="excelFile" name="excelFile" accept=".xls, .xlsx">

        <br>

        <input type="submit" value="Upload">
    </form>

</body>
</html>
    """,
    height=600,
)