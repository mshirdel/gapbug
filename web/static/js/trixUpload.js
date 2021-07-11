(function () {
    var mediaPath = '/media/'
    var HOST = "/trix/upload/";

    addEventListener("trix-attachment-add", function (event) {
        if (event.attachment.file) {
            if (event.attachment.file.type.startsWith('image'))
                uploadFileAttachment(event.attachment);
            else {
                alert('Just upload image file. please.');
            }
        }
    });

    function uploadFileAttachment(attachment) {
        uploadFile(attachment.file, setProgress, setAttributes);

        function setProgress(progress) {
            attachment.setUploadProgress(progress);
        }

        function setAttributes(attributes) {
            attachment.setAttributes(attributes);
        }
    }

    function uploadFile(file, progressCallback, successCallback) {
        var key = createStorageKey(file);
        var formData = createFormData(key, file);
        var xhr = new XMLHttpRequest();

        xhr.open("POST", HOST, true);
        xhr.setRequestHeader("X-CSRFToken", Cookies.get("csrftoken"));

        xhr.upload.addEventListener("progress", function (event) {
            var progress = (event.loaded / event.total) * 100;
            progressCallback(progress);
        });

        xhr.addEventListener("load", function (event) {
            if (xhr.status == 200) {
                var attributes = {
                    url: mediaPath + key,
                    href: mediaPath + key + "?content-disposition=attachment",
                };
                successCallback(attributes);
            }
        });

        xhr.send(formData);
    }

    function createStorageKey(file) {
        var date = new Date();
        var day = date.toISOString().slice(0, 10);
        var name = date.getTime() + "-" + file.name;
        return [day, name].join("-");
    }

    function createFormData(key, file) {
        var data = new FormData();
        data.append("key", key);
        data.append("content_type", file.type);
        data.append("file", file);
        return data;
    }
})();
