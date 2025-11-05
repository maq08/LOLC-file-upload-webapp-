let upload_id = localStorage.getItem('upload_id');
if (!upload_id) {
  upload_id = crypto.randomUUID();
  localStorage.setItem('upload_id', upload_id);
}

function showMessage(success, message) {
  const alertType = success ? 'alert-success' : 'alert-danger';
  $('#msgBox').html(`<div class="alert ${alertType} text-center">${message}</div>`);
}

function refreshList() {
  $.get('/list', { upload_id }, res => {
    const list = $('#fileList').empty();
    if (!res.files || res.files.length === 0) {
      list.append(`<li class="list-group-item text-muted text-center">No files uploaded yet.</li>`);
      return;
    }
    res.files.forEach(f => {
      const sizeKB = Math.round(f.size_bytes / 1024);
      list.append(`
        <li class="list-group-item d-flex justify-content-between align-items-center">
          <span><b>${f.filename}</b> (${sizeKB} KB) - ${f.status}</span>
          <button class="btn btn-sm btn-outline-danger" onclick="removeFile('${f.stored_name}')">Remove</button>
        </li>
      `);
    });
  });
}

$('#uploadBtn').click(() => {
  const file = $('#fileInput')[0].files[0];
  if (!file) return showMessage(false, 'Please select a file to upload.');
  if (file.size > 500 * 1024) return showMessage(false, 'File too large! Maximum size is 500KB.');

  const fd = new FormData();
  fd.append('file', file);
  fd.append('upload_id', upload_id);

  $.ajax({
    url: '/upload',
    type: 'POST',
    data: fd,
    processData: false,
    contentType: false,
    success: res => {
      showMessage(res.success, res.message);
      $('#fileInput').val('');
      refreshList();
    },
    error: err => {
      const msg = err.responseJSON?.message || 'Upload failed';
      showMessage(false, msg);
    }
  });
});

function removeFile(stored_name) {
  $.post('/remove', { upload_id, stored_name }, res => {
    showMessage(res.success, res.message);
    refreshList();
  });
}

$('#finalBtn').click(() => {
  $.post('/final_submit', { upload_id }, res => {
    showMessage(res.success, res.message);
    if (res.success) {
      localStorage.removeItem('upload_id');
      setTimeout(() => location.reload(), 1500);
    }
  });
});

$('#cancelBtn').click(() => {
  $.post('/cancel', { upload_id }, res => {
    showMessage(res.success, res.message);
    localStorage.removeItem('upload_id');
    setTimeout(() => location.reload(), 1500);
  });
});

$(document).ready(refreshList);
