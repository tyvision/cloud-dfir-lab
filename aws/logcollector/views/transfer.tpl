<html>
<body>

<style>
a {
    display: block;
}
</style>

<h1>Enter transfer specification</h1>
<p>Make sure to first configure AWS security credentials:<p>
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

<br>

<p>Example: </p>
<pre>
<code>
{
    "logstream" : [
        {
            "region" : "us-east-2"
            , "group" : "artem-vpc"
            , "stream" : "eni-049f734adb12b5de9-all"
            , "cleanup-plugin": "vpc"
        }
        , {
            "region" : "us-east-2"
            , "group" : "artem-vpc"
            , "stream" : "eni-0179683f4c01c060a-all"
            , "cleanup-plugin": "vpc"
        }
    ]
    , "s3" : [ ]
    , "metric" : [ ]
}
</code>
</pre>

</body>
</html>
