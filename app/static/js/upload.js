(function() {

var f = document.getElementById('f');
if (f.files.length)
  processFile();

f.addEventListener('change', processFile, false);


function processFile(e) {
  var file = f.files[0];
  var size = file.size;
  var sliceSize = (1000*1024)*10;
  var expectedSlice = Math.ceil(size/sliceSize);
  var promiseId = uuidv4()
  console.log("Unique Id", promiseId);
  var start = 0;
  setTimeout(loop, 1);
  var loop_set = 0;

  function loop() {
    var end = start + sliceSize;
    loop_set = loop_set + 1;
    if (size - end < 0) {
      end = size;
    }
    
    var s = slice(file, start, end);

    send(s, start, end, promiseId, expectedSlice, loop_set);

    if (end < size) {
      start += sliceSize;
      setTimeout(loop, 1);
    }
  }
}


function send(piece, start, end, promiseId, expectedSlice, loop_set) {
  var formdata = new FormData();
  var xhr = new XMLHttpRequest();

  xhr.open('POST', '/service/s3/upload', true);
  formdata.append('start', start);
  formdata.append('promiseId', promiseId);
  formdata.append('expectedSlice', expectedSlice);
  formdata.append('currentLoopId', loop_set);
  formdata.append('end', end);
  formdata.append('files', piece);
  
  xhr.send(formdata);
}

/**
 * Generating Unique Ids
 */
function uuidv4() {
  return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
    (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
  )
}

/**
 * Formalize file.slice
 */

function slice(file, start, end) {
  var slice = file.mozSlice ? file.mozSlice :
              file.webkitSlice ? file.webkitSlice :
              file.slice ? file.slice : noop;
  
  return slice.bind(file)(start, end);
}

function noop() {
  
}

})();