(function () {
    var txtSearch = document.getElementById("txtSearch");
    if (txtSearch) {
        var searchTooltip = new bootstrap.Popover(txtSearch, {
            content: `<div class="row">
                        <div class="col">[تگ] <span class="question-stats">جستجو بر اساس تگ</span></div>
                        <div class="col">answers:0 <span class="question-stats">جستجو در پرسش‌های بی پاسخ</span></div>
                    </div>
                    <div class="row">
                        <div class="col">user:1234 <span class="question-stats">جستجو بر اساس نویسنده پرسش</span></div>
                        <div class="col">score:3 <span class="question-stats">پرسش‌هایی که امتیاز آنها بیش از ۳ است</span></div>
                    </div>
                    <div class="row">
                        <div class="col">"words here" <span class="question-stats">جستجو عبارت قرار گرفته در گیومه</span></div>
                        <div class="col">isaccepted:yes|no <span class="question-stats">جستجو بر اساس وضعیت تایید پاسخ</span></div>
                    </div>`,
            placement: "bottom",
            html: true,
            trigger: "manual",
        });
        txtSearch.addEventListener("focus", function () {
            searchTooltip.show();
        });

        txtSearch.addEventListener("focusout", function () {
            searchTooltip.hide();
        });

        txtSearch.addEventListener("keyup", function (event) {
            if (event.keyCode === 13 && txtSearch.value !== '') {
                event.preventDefault();
                document.getElementById("searchForm").submit();
                
                return false;
            }
        });
    }
})();
