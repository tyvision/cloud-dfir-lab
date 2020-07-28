<html>
<body>

<style>
a {
    display: block;
}
</style>

<h1>Configure logcollector options</h1>

<form method="post" action="/action/settings">
    AWS_ACCESS_KEY_ID:      <input name="aws_access_key_id" type="text" />
    AWS_SECRET_ACCESS_KEY:  <input name="aws_secret_access_key" type="password" />
    <input value="Submit" type="submit" />
</form>

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
