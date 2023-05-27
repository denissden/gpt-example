using System.Text.Json;

namespace Deps.Contracts;

public class JsonStore
{
    public long BotId { get; set; }
    public long UserId { get; set; }
    public long ChatId { get; set; }
    public string Key { get; set; }
    public JsonElement JsonValue { get; set; }
}


public class JsonGetRequest
{
    public long BotId { get; set; }
    public long UserId { get; set; }
    public long ChatId { get; set; }
    public string Key { get; set; }
}

public class JsonGetResponse : JsonStore
{
    public DateTime CreatedAt { get; set; }
}