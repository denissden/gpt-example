using System.Text.Json.JsonDiffPatch;
using Deps.Contracts;
using Mapster;
using MassTransit;
using Microsoft.EntityFrameworkCore;
using State.Models;

namespace State.Consumers;

public class JsonStoreConsumer : IConsumer<JsonStore>
{
    private readonly StateDbContext _context;

    public JsonStoreConsumer(StateDbContext context)
    {
        _context = context;
    }

    public async Task Consume(ConsumeContext<JsonStore> context)
    {
        var msg = context.Message;
        
        var entry = await _context.Set<JsonEntry>()
            .Where(s => s.BotId == msg.BotId)
            .Where(s => s.ChatId == msg.ChatId)
            .Where(s => s.UserId == msg.UserId)
            .Where(s => s.Key == msg.Key)
            .OrderByDescending(s => s.Id)
            .FirstOrDefaultAsync();
        if (entry is not null && entry.JsonValue.DeepEquals(msg.JsonValue))
            entry.UpdatedAt = DateTime.UtcNow;
        else
            entry = msg.Adapt(new JsonEntry { CreatedAt = DateTime.UtcNow });

        _context.Update(entry);
        await _context.SaveChangesAsync();
    }
}