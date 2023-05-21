var imgUpload = document.getElementById('inputImage'), 
imgPreview = document.getElementById('img-preview'), 
imgUploadForm = document.getElementById('form-upload'), 
totalFiles, previewTitle, previewTitleText, img;
​
imgUpload.addEventListener('change', previewImgs, true);
​
​
​
var selectedFiles = []; 
​
function previewImgs(event) {
  var previewContainer = document.getElementById('img-preview');
  previewContainer.innerHTML = ''; 
​
  var files = event.target.files;
  var totalFiles = files.length;
​
  if (!!totalFiles) {
    imgPreview.classList.remove('img-thumbs-hidden');
  }
​
  selectedFiles = Array.from(files); 
  for (var i = 0; i < totalFiles; i++) {
    var wrapper = document.createElement('div');
    wrapper.classList.add('wrapper-thumb');
    var removeBtn = document.createElement('span');
    var nodeRemove = document.createTextNode('x');
    removeBtn.classList.add('remove-btn');
    removeBtn.appendChild(nodeRemove);
    var img = document.createElement('img');
    img.src = URL.createObjectURL(files[i]);
    img.classList.add('img-preview-thumb');
    wrapper.appendChild(img);
    wrapper.appendChild(removeBtn);
    previewContainer.appendChild(wrapper);
​
    removeBtn.addEventListener('click', function (e) {
      var parentWrapper = e.target.parentNode;
      var imageIndex = Array.prototype.indexOf.call(previewContainer.children, parentWrapper);
      parentWrapper.remove();
      console.log(imageIndex);
      if (imageIndex !== -1) {
        selectedFiles.splice(imageIndex, 1);
      }
      totalFiles = selectedFiles.length;
      if (totalFiles === 0) {
        imgPreview.classList.add('img-thumbs-hidden');
      }
    });
  }
}