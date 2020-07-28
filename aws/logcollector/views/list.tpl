<html>
<body>

<style>
a {
    display: block;
}
</style>

<script>
function getStorage(storage) {
    document.getElementById('list').innerHTML = "Loading can take up to 30 seconds...";

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4){
            document.getElementById('list').innerHTML = xhr.responseText;
        }
    };
    xhr.open('GET', '/action/' + storage);
    xhr.send();
}
</script>

<h1>View available items</h1>
<p>Make sure to first configure AWS security credentials:<p>
<a href="/display/settings">Settings</a>

<br>

<textarea id="list" wrap="off" rows="30" cols="80"></textarea>

<br>

%if storage == 's3':
<button type="button" onclick="getStorage('s3')">Update list of S3 buckets </button>
%elif storage == "logstream":
<button type="button" onclick="getStorage('logstream')">Update list of Log Streams</button>
%elif storage == "cloudwatch":
<button type="button" onclick="getStorage('cloudwatch')">Update list of Cloud Watch Metrics</button>
%end

<br>

<p>View availiable items:<p>
<a href="/display/s3">S3 Buckets</a>
<a href="/display/logstream">Log Streams</a>
<a href="/display/cloudwatch">Cloud Watch Metrics</a>

<br>

<p>Submit prepared transfer specification:<p>
<a href="/display/transfer">Transfer</a>

</body>
</html>
