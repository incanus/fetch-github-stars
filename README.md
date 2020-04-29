# fetch-github-stars

This is a little Python script to use the [GitHub v3 REST API](https://developer.github.com/v3/) to download a user's starred repositories and put the public ones into a compact JSON format on disk, suitable for inclusion in a [Hugo](https://gohugo.io) or similar blog engine (on which you can also create an RSS feed). For now, I run this script periodically when publishing other things on my site. 

It will load up previously-seen results each time and quit early if it gets a bank of results that have been partially- or entirely-seen already, since it fetches the newest stuff first. 

This doesn't need a GitHub account or developer token since this is public data. 

See the top of the script to specify the user whose data you want to fetch and where to store that data on disk. 

## Requirements

You'll need to `pip3 install requests` since [Requests](https://requests.readthedocs.io/en/master/) is required. 

## Use in Hugo

Here's how I use the fetched data on [my Hugo-based site](https://justinmiller.io/links/): 

```go
<div class="posts">
{{ range .Site.Data.github_stars.projects -}}
<article class="post">
  <h2 class="post-title">
    <a href="{{ .url }}">{{ .name }}</a>
  </h2>
  <p>{{ .description }}</p>
  {{- $utc := time .date -}}
  {{- $utcstamp := $utc.Unix -}}
  {{- $date := time $utcstamp -}}
  <time datetime="{{ $date.Format "2006-01-02T15:04:05Z0700" }}" class="post-date">{{ $date.Format "Mon, Jan 2, 2006 at 3:04pm" }}</time>
</article>
{{- end }}
</div>
```

The little time & date song-and-dance is because the data is in UTC and I want to display it in my home timezone. 

Similarly, you could use this data in a personally-hosted RSS feed of your starred repositories, as [I have done](https://justinmiller.io/links.xml). 
