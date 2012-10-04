${include file="partials/doctype.html.tpl" /}
<head>
    <title>Hive Solutions - The diary</title>
    ${include file="partials/includes.html.tpl" /}
</head>
<body>
    ${include file="partials/header.html.tpl" /}
    ${include file="partials/windows.html.tpl" /}
    <div id="wrapper">
        <div id="content-column">
            ${include file_value=page_include /}
        </div>
        ${include file="partials/side_panel.html.tpl" /}
    </div>
    ${include file="partials/footer.html.tpl" /}
</body>
${include file="partials/end_doctype.html.tpl" /}
