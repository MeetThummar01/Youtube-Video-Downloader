const urlInput = document.getElementById("url");
const downloadBtn = document.getElementById("download");

downloadBtn.onclick = async () => {
  const url = urlInput.value;
  const res = await fetch(`/api/download?url=${encodeURIComponent(url)}`);
  
  if (res.ok) {
    const blob = await res.blob();
    const a = document.createElement("a");
    a.href = window.URL.createObjectURL(blob);
    a.download = "video.mp4";
    a.click();
  } else {
    const data = await res.json();
    alert("Error: " + data.error);
  }
};
