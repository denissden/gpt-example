using Deps.Contracts;
using Mapster;
using MassTransit;
using Microsoft.EntityFrameworkCore;
using State.Models;

namespace State.Consumers;

public class JsonGetRequestConsumer : IConsumer<JsonGetRequest>
{
    private readonly StateDbContext _context;

    public JsonGetRequestConsumer(StateDbContext context)
    {
        _context = context;
    }

    public async Task Consume(ConsumeContext<JsonGetRequest> context)
    {
        var msg = context.Message;
        var entry = await _context.Set<JsonEntry>()
            .Where(s => s.BotId == msg.BotId)
            .Where(s => s.ChatId == msg.ChatId)
            .Where(s => s.UserId == msg.UserId)
            .Where(s => s.Key == msg.Key)
            .OrderByDescending(s => s.Id)
            .FirstOrDefaultAsync();

        var response = entry?.Adapt<JsonGetResponse>();
        await context.RespondAsync(new[] { response });
    }
}