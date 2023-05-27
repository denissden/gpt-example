using Microsoft.EntityFrameworkCore;
using State.Models;

namespace State;

public class StateDbContext : DbContext
{
    public StateDbContext(DbContextOptions<StateDbContext> options) : base(options)
    {
        
    }
    
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        modelBuilder.Entity<JsonEntry>()
            .Property(e => e.JsonValue)
            .HasColumnType("jsonb");
    }
}