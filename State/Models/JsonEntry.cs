using System.Text.Json;

namespace State.Models;

public class JsonEntry
{
    public long Id { get; set; }
    public long BotId { get; set; }
    public long UserId { get; set; }
    public long ChatId { get; set; }
    public string Key { get; set; }
    public JsonElement JsonValue { get; set; }
    
    public DateTime CreatedAt { get; set; }
    public DateTime? UpdatedAt { get; set; }
}