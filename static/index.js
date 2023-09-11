
function showCancelingMessage() {
    document.getElementById('canceling-message').style.display = 'block';
    setTimeout(function() {
      document.getElementById('canceling-message').style.display = 'none';
    }, 6000); 
  }
  