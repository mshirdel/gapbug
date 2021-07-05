let dropArea = document.getElementById("drop-area");
let selectedFile = null;

["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
    dropArea.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

["dragenter", "dragover"].forEach((eventName) => {
    dropArea.addEventListener(eventName, highlight, false);
});

["dragleave", "drop"].forEach((eventName) => {
    dropArea.addEventListener(eventName, unhighlight, false);
});

function highlight(e) {
    dropArea.classList.add("highlight");
}

function unhighlight(e) {
    dropArea.classList.remove("highlight");
}

dropArea.addEventListener("drop", handleDrop, false);

function handleDrop(e) {
    let dt = e.dataTransfer;
    let files = dt.files;
    selectedFile = files.item(0);
    previewFile(selectedFile);
}

function handleFiles(files) {
    selectedFile = files.item(0);
    previewFile(selectedFile);
}

function uploadFile(file) {
    let url = "/users/avatar/upload/";
    let formData = new FormData();

    formData.append("avatar", file);
    fetch(url, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "Accept": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": Cookies.get("csrftoken"),
        },
        body: formData,
    })
        .then((response) => {
            if (response.url) {
                window.location.href = response.url;
            }
        })
        .catch((e) => {
            console.log(e);
        });
}

function uploadSelectedFile() {
    if (selectedFile) {
        uploadFile(selectedFile);
    }
}

function previewFile(file) {
    let reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = function () {
        let img = document.createElement("img");
        img.src = reader.result;
        img.classList.add("img-thumbnail");
        let gallery = document.getElementById("gallery");
        if (gallery.children.length > 0) {
            gallery.removeChild(gallery.firstChild);
        }
        gallery.appendChild(img);
    };
}
