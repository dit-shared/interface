var imageCounter = 0;

document.getElementById("imageBox").src = '/media/images/{{ series.media_path }}/0.png';

function previous() {
  imageCounter--;
  if(imageCounter < 0) {
    imageCounter = {{ voxels.shape.2|add:"-1" }};
  }
  document.getElementById("imageCounter").innerHTML = imageCounter+1;
  document.getElementById("imageBox").src = '/media/images/{{ series.media_path }}/' + imageCounter + '.png';
}

function next() {
    imageCounter++;
    if(imageCounter >= {{ voxels.shape.2 }}) {
      imageCounter = 0;
    }
    document.getElementById("imageCounter").innerHTML = imageCounter+1;
    document.getElementById("imageBox").src = '/media/images/{{ series.media_path }}/' + imageCounter + '.png';
}