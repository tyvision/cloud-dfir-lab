<html>
<body>

<style>
a {
    display: block;
}
</style>

<h1>Enter transfer specification</h1>
<p>Make sure to first configure AWS/GCP security credentials:<p>
<a href="/display/settings">Settings</a>

<br>

<form method="post" action="/action/transfer">
    <textarea wrap="off" name="transfer_spec" rows="10" cols="80"></textarea>
    <input type="datetime-local" name="timestart" value="2000-01-01T00:01:00">
    <input type="datetime-local" name="timeend" value="3000-01-01T00:01:00">
    <input type="submit" value="Submit spec">
</form>

<br>

<p>View availiable items:<p>
<a href="/display/s3">S3 Buckets</a>
<a href="/display/logstream">Log Streams</a>
<a href="/display/cloudwatch">Cloud Watch Metrics</a>
<a href="/display/gcp-bucket">GCP Bucket Blobs</a>

<br>

<p>Example: </p>
<pre>
<code>

{
    "cloud": "aws"
    , "storage" : "logstream"
    , "cleanup": "vpc"
    , "region" : "us-east-2"
    , "group" : "artem-vpc"
    , "stream" : "eni-049f734adb12b5de9-all"
}
{
    "cloud": "aws"
    , "storage" : "logstream"
    , "cleanup": "vpc"
    , "region" : "us-east-2"
    , "group" : "artem-vpc"
    , "stream" : "eni-049f734adb12b5de9-all"
}
{
    "cloud": "gcp"
    , "storage" : "bucket"
    , "cleanup": "cloudaudit"
    , "bucket" : "save-logs"
    , "prefix" : "cloudaudit.googleapis.com/activity/2020/07/28/21:00:00_21:59:59_S0.json"
}
{
    "cloud": "gcp"
    , "storage" : "bucket"
    , "cleanup": "cloudaudit"
    , "bucket" : "images-exports"
    , "prefix" : "cloudaudit.googleapis.com/activity/2020/07/10/15:00:00_15:59:59_S0.json"
}


</code>
</pre>

</body>
</html>
