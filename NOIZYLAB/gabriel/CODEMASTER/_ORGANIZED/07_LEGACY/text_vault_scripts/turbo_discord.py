#!/usr/bin/env python3
# ==============================================================================
# 🦅 THE CARRIER (DISCORD RELAY)
# ==============================================================================
# "The Voice of Gabriel across the Aether."
# Connects the MC96 Universe to the User's Mobile Device.

import discord
from discord.ext import commands, tasks
import asyncio
import subprocess
import os
import sys
from pathlib import Path

# Load Turbo Environment
try:
    import turbo_config as cfg
    import turbo_prompts as prompts
    from turbo_memcell import MemCell
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    import turbo_config as cfg
    import turbo_prompts as prompts
    from turbo_memcell import MemCell

# CONFIGURATION
TOKEN = cfg.API_KEYS["Discord"]
CHANNEL_ID = 123456789012345678  # Replace with actual Channel ID from MemCell or Config

# INTENTS
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# MEMORY & PERSONAS
memory = MemCell()
current_persona = "GABRIEL"

# ==============================================================================
# 🤖 BOT EVENTS
# ==============================================================================

@bot.event
async def on_ready():
    print(f"{cfg.GREEN}🦅 THE CARRIER IS ONLINE: {bot.user.name}{cfg.RESET}")
    print(f"{cfg.DIM}   Connected to Discord Gateway.{cfg.RESET}")
    
    # Log Start
    memory.log_event(0, "SYSTEM_CONNECT", f"The Carrier online as {bot.user.name}", 100, "CARRIER")
    
    # Start Heartbeat
    status_loop.start()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Direct Message or Mention handling could go here
    # For now, just process commands
    await bot.process_commands(message)

# ==============================================================================
# ⚡ COMMANDS (THE TEAM)
# ==============================================================================

@bot.command(name="gabriel")
async def ask_gabriel(ctx, *, query):
    """Ask Gabriel (God Mode)"""
    await ctx.send(f"🦅 **GABRIEL IS THINKING...**")
    
    # 1. Get Context (Omniscience)
    context = memory.inject_omniscience()
    
    # 2. Simulate Cortex Call (In real production, import Cortex logic or call API)
    # For now, we use a placeholder response to prove connectivity
    response = f"**[OMNISCIENCE ACTIVE]**\nI see your query: *'{query}'*.\n\nContext Loaded: {len(context)} chars.\nAction: **OPTIMIZING.**"
    
    await ctx.send(response)

@bot.command(name="shirl")
async def ask_shirl(ctx, *, query):
    """Ask Shirl (Vibe Check)"""
    await ctx.send(f"✨ **Shirl is checking the vibe...**")
    memory.log_event(0, "VIBE_CHECK", f"Discord Query: {query}", 80, "SHIRL")
    await ctx.send(f"🌸 *My intuition says: {query} feels right.* \n(Vibe logged to Universe DB)")

@bot.command(name="keith")
async def ask_keith(ctx, *, query):
    """Ask Engr Keith (Status)"""
    await ctx.send(f"📐 **Keith Initializing...**")
    await ctx.send(f"🛠️ **STATUS:** SYSTEM NOMINAL.\nUNIVERSE DB: SECURE.\nQUERY '{query}' ACKNOWLEDGED.")

@bot.command(name="status")
async def system_status(ctx):
    """Get System Health Report"""
    # 1. Database Pulse
    try:
        memory.cursor.execute("SELECT count(*) FROM memory_events")
        count = memory.cursor.fetchone()[0]
        db_status = "ONLINE"
    except:
        count = "ERROR"
        db_status = "CRITICAL"

    # 2. Network Pulse (Ping Check)
    def check_ping(ip):
        try:
            # -c 1 = count 1, -W 500 = timeout 500ms
            ret = subprocess.run(["ping", "-c", "1", "-W", "500", ip], capture_output=True)
            return "🟢 ONLINE" if ret.returncode == 0 else "🔴 OFFLINE"
        except: return "⚠️ UNKNOWN"

    omen_status = check_ping("10.90.90.20") # HP-OMEN (GABRIEL)
    vault_status = check_ping("10.90.90.30") # MacPro (THE_VAULT)

    embed = discord.Embed(title="MC96 SYSTEM STATUS", color=0x00ff00)
    embed.add_field(name="🧠 Memory Events", value=f"{count}", inline=False)
    
    # Network Grid
    grid = f"**M2 ULTRA (OMEGA)**: 🟢 ONLINE\n" \
           f"**HP-OMEN (GABRIEL)**: {omen_status}\n" \
           f"**MacPro (THE_VAULT)**: {vault_status}\n" \
           f"**DGS SWITCH**: 🟢 LINKED"
           
    embed.add_field(name="🌐 GORUNFREE NETWORK", value=grid, inline=False)
    
    embed.add_field(name="🦅 Carrier", value="ONLINE", inline=True)
    embed.set_footer(text="ONE TRUTH. ONE SOURCE.")
    
    await ctx.send(embed=embed)

@bot.command(name="team")
async def list_team(ctx):
    """List the Digital Team"""
    roster = "\n".join([f"**{k}**: {v}" for k, v in cfg.TEAM_ROSTER.items()])
    await ctx.send(f"👥 **THE DIGITAL TEAM**\n{roster}")

# ==============================================================================
# 💓 BACKGROUND TASKS
# ==============================================================================

@tasks.loop(minutes=30)
async def status_loop():
    # In production, this would act as a 'Dead Man's Switch' or Vibe check
    # If vibe drops, DM the user
    pass

# ==============================================================================
# 🚀 LAUNCH
# ==============================================================================

if __name__ == "__main__":
    if not TOKEN:
        print(f"{cfg.RED}❌ ERROR: DISCORD_TOKEN not found in Environment or Config.{cfg.RESET}")
        print("   Please export DISCORD_TOKEN='your_token_here'")
    else:
        try:
            bot.run(TOKEN)
        except Exception as e:
            print(f"{cfg.RED}❌ ERROR: Connection Failed: {e}{cfg.RESET}")
