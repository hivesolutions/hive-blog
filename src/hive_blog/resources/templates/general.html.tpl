${include file="doctype.html.tpl" /}
<head>
    <title>Hive Solutions - The diary</title>
    ${include file="includes.html.tpl" /}
</head>
<body>
    ${include file="header.html.tpl" /}
    ${include file="windows.html.tpl" /}
    <div id="wrapper">
        <div id="content-column">
            ${include file_value=page_include /}
        </div>
        ${include file="side_panel.html.tpl" /}
    </div>
    ${include file="footer.html.tpl" /}
</body>
${include file="end_doctype.html.tpl" /}
