<div id="footer">
    <a id="copyright" href="http://hive.pt">&copy; Hive Solutions Lda - All rights reserved</a>
    <a id="powered-by" href="http://getcolony.com"></a>
    ${if item=session.user value=None operator=neq}
        <div id="logged">
            currently logged in as ${out value=session.user xml_escape=True /}
            // <a href="${out value=base_path /}logout">logout</a>
        </div>
    ${/if}
</div>

<!-- analytics inclusion -->
${include file="google_analytics.html.tpl" /}
