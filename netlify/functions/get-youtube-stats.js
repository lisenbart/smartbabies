// Netlify Function: Fetch public YouTube channel statistics
// Requires environment variables:
// - YOUTUBE_API_KEY: YouTube Data API v3 key
// - YOUTUBE_CHANNEL_ID: Channel ID (e.g., UCxxxxxxxxxxxx)

exports.handler = async function(event, context) {
  const apiKey = process.env.YOUTUBE_API_KEY;
  const channelId = process.env.YOUTUBE_CHANNEL_ID;

  if (!apiKey || !channelId) {
    return {
      statusCode: 400,
      body: JSON.stringify({ error: 'Missing YOUTUBE_API_KEY or YOUTUBE_CHANNEL_ID env vars' })
    };
  }

  const url = `https://www.googleapis.com/youtube/v3/channels?part=statistics&id=${encodeURIComponent(channelId)}&key=${encodeURIComponent(apiKey)}`;

  try {
    const res = await fetch(url);
    if (!res.ok) {
      const text = await res.text();
      return { statusCode: res.status, body: JSON.stringify({ error: 'YouTube API error', detail: text }) };
    }
    const data = await res.json();
    const stats = data.items && data.items[0] && data.items[0].statistics ? data.items[0].statistics : null;

    if (!stats) {
      return { statusCode: 404, body: JSON.stringify({ error: 'Stats not found' }) };
    }

    // Note: YouTube Data API provides total counts, not 30-day metrics (needs Analytics API/OAuth)
    const payload = {
      viewCount: Number(stats.viewCount || 0),
      subscriberCount: Number(stats.subscriberCount || 0),
      hiddenSubscriberCount: Boolean(stats.hiddenSubscriberCount),
      videoCount: Number(stats.videoCount || 0)
    };

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' },
      body: JSON.stringify(payload)
    };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: 'Server error', detail: String(err) }) };
  }
};


