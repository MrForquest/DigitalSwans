
const modal = document.getElementById("myModal");
const modalText = document.getElementById("modal-text");
const closeBtn = document.getElementsByClassName("close")[0];
const fileURL = document.getElementById("file");
const forms = document.querySelectorAll("form");
const fileInput = document.getElementById("file");
const label = document.querySelector("label[for='file']");
const originalText = label.textContent;
const cancel = document.getElementById("cancel");
const preloader = document.getElementById("preloader");
const reset = document.getElementById("reset")


document.addEventListener("DOMContentLoaded", () => {
    (function(){
        let files, 
            file, 
            extension,
            input = document.getElementById("file"), 
            output = document.getElementById("fileOutput");

            input.addEventListener("change", function(e) {
            files = e.target.files;
            output.innerHTML = "";

            for (var i = 0, len = files.length; i < len; i++) {
            file = files[i];
            extension = file.name.split(".").pop();
            output.innerHTML += "<li class='type-" + extension + "'>" + file.name + "</li>";
            }
            }, false);
            })();






// обработчик события "change" (происходит после выбора файла)
fileURL.addEventListener("change", () => {
    uploadFile(fileURL.files[1].path);
});

// Загрузка файла
const uploadFile = (file) => {
    console.log(file);
};

// отправляем `POST` запрос
const postData = async (url, fData) => { // имеет асинхронные операции

// ждём ответ, только тогда наш код пойдёт дальше
let fetchResponse = await fetch("http://localhost:58513/load_path", {
   method: "POST",
   body: fData

}).then((response) => {
    
    if (response.ok) {
        return response.text();
    } else {
        throw new Error("Server response wasn't OK");
        
    }
    })
    .then((data) => {
        preloader.style.display = "none";
        const fin = JSON.parse(data)
        modalText.innerHTML = fin.creatures.map((obj) => 
            ` <p class="module_text" style="padding-left:"0.5em"> ${obj.ru_name}: ${obj.number} штук </p>`
        ).join("");

        modalText.innerHTML += `<p><a class="upload" onclick="downloadFile('${fin.detail_info_src}', '.\\filename.csv')">Скачать подробные данные</a></p>`
        showModal();
    })
    .catch((error) => {
        console.error(error);
    });

};


function showModal() {
  modal.style.display = "block";
}

function hideModal() {
  modal.style.display = "none";
}
function saveFile(url) {
    console.log(url)
}
console.log(saveFile)
closeBtn.onclick = hideModal;


if (forms) {
forms.forEach(el => {
   el.addEventListener("submit", function (e) {
       e.preventDefault();

        preloader.style.display = "block";
        el.style.display = "none";
        
      
       // создание объекта FormData
       const fData = new FormData(el);
       fData.append("dir_path", fileURL.files[1].path);
      
       // Отправка на сервер
       postData("http://localhost:58513/load_path", fData)
           
   });
});
};
});


fileInput.addEventListener("change", function() {
    const nik = fileInput.files[0].path.split("\\");
    label.textContent = nik[nik.length-2];
});


cancel.addEventListener("click", function() {
  label.textContent = originalText;
});

reset.addEventListener("click", function() {
    forms[0].style.display = "block";
    label.textContent = originalText;
});

const https = require('https');
const fs = require('fs');

function downloadFile(url, filePath) {
  const file = fs.createWriteStream(filePath);

  https.get(url, (response) => {
    response.pipe(file);

    file.on('finish', () => {
      file.close();
      console.log(`File downloaded to ${filePath}`);
    });
  }).on('error', (err) => {
    fs.unlink(filePath, () => {}); 
    console.error(`Error downloading file: ${err.message}`);
  });
}