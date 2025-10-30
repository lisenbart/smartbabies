// Returns titles for given YouTube video IDs using YouTube Data API v3 (server-side)
// Query: /.netlify/functions/get-video-details?ids=ID1,ID2,ID3

exports.handler = async function(event) {
  const apiKey = process.env.YOUTUBE_API_KEY;
  const idsParam = (event.queryStringParameters && event.queryStringParameters.ids) || '';
  if (!apiKey) {
    return { statusCode: 400, body: JSON.stringify({ error: 'Missing YOUTUBE_API_KEY' }) };
  }
  const ids = idsParam.split(',').map(s => s.trim()).filter(Boolean);
  if (!ids.length) {
    return { statusCode: 400, body: JSON.stringify({ error: 'Missing ids query param' }) };
  }

  const url = `https://www.googleapis.com/youtube/v3/videos?part=snippet&id=${encodeURIComponent(ids.join(','))}&key=${encodeURIComponent(apiKey)}`;
  try {
    const res = await fetch(url);
    if (!res.ok) {
      const text = await res.text();
      return { statusCode: res.status, body: JSON.stringify({ error: 'YouTube API error', detail: text }) };
    }
    const data = await res.json();
    const map = {};
    if (data && Array.isArray(data.items)) {
      data.items.forEach(item => {
        if (item && item.id && item.snippet) {
          map[item.id] = item.snippet.title || '';
        }
      });
    }
    return { statusCode: 200, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' }, body: JSON.stringify(map) };
  } catch (e) {
    return { statusCode: 500, body: JSON.stringify({ error: 'Server error', detail: String(e) }) };
  }
};


