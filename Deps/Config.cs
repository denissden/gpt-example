using MassTransit;

namespace Deps;

public static class Config
{
    public static class RabbitMq
    {
        public static string Host => Environment.GetEnvironmentVariable("RABBITMQ_HOST") ?? "localhost";
        public static string Vhost => Environment.GetEnvironmentVariable("RABBITMQ_VHOST") ?? "/";
        public static string User => Environment.GetEnvironmentVariable("RABBITMQ_USER") ?? "guest";
        public static string Pass => Environment.GetEnvironmentVariable("RABBITMQ_PASS") ?? "guest";
    }
    
    public static class Database
    {
        public static string Connection => GetVariableOrComplain("POSTGRES_CONNECTION");
    }

    public static void RabbitMqFromConfig(
        this IBusRegistrationConfigurator configurator, 
        Action<IBusRegistrationContext, IRabbitMqBusFactoryConfigurator>? configure = null)
    {
        configurator.UsingRabbitMq((context, cfg) =>
        {
            cfg.Host(RabbitMq.Host, RabbitMq.Vhost, h =>
            {
                h.Username(RabbitMq.User);
                h.Password(RabbitMq.Pass);
            });
            
            configure?.Invoke(context, cfg);
        });
    }
    
    private static string GetVariableOrComplain(string variableName)
    {
        var value = Environment.GetEnvironmentVariable(variableName);
        
        if (string.IsNullOrEmpty(value))
        {
            throw new ArgumentNullException($"Environment variable {variableName} is not provided");
        }

        return value;
    }
}