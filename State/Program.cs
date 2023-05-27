using Deps;
using Deps.Contracts;
using MassTransit;
using Microsoft.EntityFrameworkCore;
using RabbitMQ.Client;
using State;

IHost host = Host.CreateDefaultBuilder(args)
    .ConfigureServices(services =>
    {
        //services.AddHostedService<Worker>();

        services.AddMassTransit(x =>
        {
            x.RabbitMqFromConfig((context, cfg) =>
            {
                // required to create consumer queues
                cfg.ConfigureEndpoints(context, new KebabCaseEndpointNameFormatter(includeNamespace: false));
                
                cfg.Message<JsonGetResponse[]>(x => x.SetEntityName("x_bot"));
            });

            x.AddConsumers(typeof(Program).Assembly);
        });

        services.AddDbContext<StateDbContext>(
            options => options.UseNpgsql(Config.Database.Connection)
        );
    })
    .Build();

using (var scope = host.Services.CreateScope())
{
    // ensure database is created
    var context = scope.ServiceProvider.GetRequiredService<StateDbContext>();
    context.Database.EnsureCreated();

    var publisher = scope.ServiceProvider.GetRequiredService<IPublishEndpoint>();
    await publisher.Publish(new JsonGetRequest
    {
        UserId = 1,
        Key = "keykey"
    });
}

await host.RunAsync();