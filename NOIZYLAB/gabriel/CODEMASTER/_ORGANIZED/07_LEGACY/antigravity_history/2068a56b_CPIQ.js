/**
 * NOIZYLAB SLACK REPAIRS WORKER (BOLT EDITION)
 * ═══════════════════════════════════════════════════════════════════════════
 * Built with @slack/bolt and slack-cloudflare-workers
 * Features: /repair command, Interactive Buttons, Assistant Events
 * ═══════════════════════════════════════════════════════════════════════════
 */

import { SlackApp } from "slack-cloudflare-workers";

export default {
  async fetch(request, env, ctx) {
    const app = new SlackApp({ env });

    // ════════════════════════════════════════════════════════════════════════
    // 🔧 COMMAND: /repair
    // ════════════════════════════════════════════════════════════════════════
    app.command("/repair", async ({ command, ack, respond, client }) => {
      await ack();

      const args = command.text.trim().split(" ");
      const subCommand = args[0]?.toLowerCase() || "help";

      switch (subCommand) {
        case "list":
          await listRepairs(env, respond);
          break;
        case "stats":
          await getStats(env, respond);
          break;
        case "add":
          await addRepair(args.slice(1), command.user_id, command.user_name, env, respond, client);
          break;
        case "auth":
          await checkAuthorizations(env, respond, client);
          break;
        case "help":
        default:
          await respond(getHelp());
      }
    });

    // ════════════════════════════════════════════════════════════════════════
    // 🖱️ ACTIONS: Buttons
    // ════════════════════════════════════════════════════════════════════════
    app.action("start_repair", async ({ action, ack, body, client, respond }) => {
      await ack();
      const repairId = action.value;
      const userId = body.user.id;

      await updateRepairStatus(repairId, "in_progress", userId, env);

      // Notify Channel
      await client.chat.postMessage({
        channel: "#repair-queue",
        text: `🔧 <@${userId}> started repair #${repairId} (Bolt Action)`
      });

      // Update the list in place
      await listRepairs(env, respond);
    });

    app.action("complete_repair", async ({ action, ack, body, client, respond }) => {
      await ack();
      const repairId = action.value;
      const userId = body.user.id;

      await updateRepairStatus(repairId, "completed", userId, env);

      await client.chat.postMessage({
        channel: "#repair-queue",
        text: `✅ <@${userId}> completed repair #${repairId} (Bolt Action)`
      });

      await listRepairs(env, respond);
    });

    // ════════════════════════════════════════════════════════════════════════
    // 🤖 EVENTS: Assistant & App Home
    // ════════════════════════════════════════════════════════════════════════
    app.event("app_home_opened", async ({ event, client }) => {
      // Placeholder for App Home Tab
      console.log("App Home Opened", event.user);
    });

    // New Assistant Capability
    app.event("assistant_thread_started", async ({ event, client }) => {
      await client.chat.postMessage({
        channel: event.assistant_thread.channel_id,
        thread_ts: event.assistant_thread.thread_ts,
        text: "👋 NoizyLab Assistant at your service! How can I help with repairs?"
      });
    });

    // Initialize logic
    return await app.run(request, ctx);
  },
};

// ═══════════════════════════════════════════════════════════════════════════
// LOGIC HELPERS
// ═══════════════════════════════════════════════════════════════════════════

async function listRepairs(env, respond) {
  const { results } = await env.DB.prepare(`
    SELECT * FROM repairs 
    WHERE status != 'completed' 
    ORDER BY priority DESC, created_at ASC
    LIMIT 20
  `).all();

  if (!results || results.length === 0) {
    await respond({
      response_type: "ephemeral",
      text: "📋 No active repairs in queue. Nice work! 🎉"
    });
    return;
  }

  const blocks = [
    { type: "header", text: { type: "plain_text", text: "🔧 Active Repairs", emoji: true } },
    { type: "divider" }
  ];

  for (const repair of results) {
    const statusEmoji = repair.status === "in_progress" ? "🟡" : "⚪";
    const priorityEmoji = repair.priority >= 3 ? "🔴" : repair.priority === 2 ? "🟠" : "⚪";

    blocks.push({
      type: "section",
      text: {
        type: "mrkdwn",
        text: `${statusEmoji} *#${repair.id}* - ${repair.device_type}\n${priorityEmoji} ${repair.description}\n💰 $${repair.price || 0}`
      },
      accessory: {
        type: "button",
        text: {
          type: "plain_text",
          text: repair.status === "in_progress" ? "✅ Complete" : "▶️ Start",
          emoji: true
        },
        action_id: repair.status === "in_progress" ? "complete_repair" : "start_repair",
        value: String(repair.id),
        style: repair.status === "in_progress" ? "primary" : undefined
      }
    });
  }

  await respond({
    response_type: "in_channel",
    blocks: blocks
  });
}

async function getStats(env, respond) {
  const today = new Date().toISOString().split("T")[0];

  const { results: todayResults } = await env.DB.prepare(`
    SELECT COUNT(*) as count, SUM(price) as revenue FROM repairs 
    WHERE status = 'completed' AND DATE(completed_at) = ?
  `).bind(today).all();

  const { results: pendingResults } = await env.DB.prepare(`
    SELECT COUNT(*) as count FROM repairs WHERE status != 'completed'
  `).all();

  const { results: weeklyResults } = await env.DB.prepare(`
    SELECT COUNT(*) as count, SUM(price) as revenue FROM repairs 
    WHERE status = 'completed' AND completed_at >= datetime('now', '-7 days')
  `).all();

  const todayCount = todayResults[0]?.count || 0;
  const todayRevenue = todayResults[0]?.revenue || 0;
  const pendingCount = pendingResults[0]?.count || 0;
  const weeklyCount = weeklyResults[0]?.count || 0;
  const weeklyRevenue = weeklyResults[0]?.revenue || 0;

  const target = 12;
  const progress = Math.min(todayCount, target);
  const progressBar = "█".repeat(progress) + "░".repeat(target - progress);

  await respond({
    response_type: "in_channel",
    blocks: [
      { type: "header", text: { type: "plain_text", text: "📊 Repair Stats", emoji: true } },
      { type: "divider" },
      {
        type: "section",
        text: {
          type: "mrkdwn",
          text: `*Today's Progress:*\n🎯 ${todayCount}/${target} repairs\n[${progressBar}]\n💰 $${todayRevenue.toFixed(2)} revenue`
        }
      },
      {
        type: "section",
        text: {
          type: "mrkdwn",
          text: `*Queue:* ${pendingCount} repairs waiting\n*This Week:* ${weeklyCount} repairs | $${weeklyRevenue.toFixed(2)}`
        }
      },
      {
        type: "context",
        elements: [{ type: "mrkdwn", text: `⚡ GORUNFREE x1000 | ${new Date().toLocaleString()}` }]
      }
    ]
  });
}

async function addRepair(args, userId, userName, env, respond, client) {
  if (args.length < 2) {
    await respond({
      response_type: "ephemeral",
      text: '❌ Usage: `/repair add <device> "<description>" [price] [priority 1-3]`'
    });
    return;
  }

  const device = args[0];
  const description = args.slice(1, -2).join(" ").replace(/"/g, "") || args[1];
  const price = parseFloat(args[args.length - 2]) || 0;
  const priority = parseInt(args[args.length - 1]) || 1;

  await env.DB.prepare(`
    INSERT INTO repairs (device_type, description, price, priority, status, created_by, created_at)
    VALUES (?, ?, ?, ?, 'pending', ?, datetime('now'))
  `).bind(device, description, price, priority, userName).run();

  // Bolt Client for Posting to Channel
  try {
    await client.chat.postMessage({
      channel: "#repair-queue",
      text: `📥 New repair added by <@${userId}>:\n*${device}* - ${description} | $${price}`
    });
  } catch (e) {
    console.error("Failed to post to #repair-queue", e);
  }

  await respond({
    response_type: "ephemeral",
    text: `✅ Repair added: ${device} - ${description}`
  });
}

async function checkAuthorizations(env, respond, client) {
  try {
    // Bolt's client handles the token automatically if configured, 
    // but apps.event.authorizations.list requires App-Level Token
    // We can use the client to call generic methods
    const result = await client.apps.event.authorizations.list({
      event_context: "123" // This API actually requires an event_context usually,
      // but listing all is restricted. 
      // For general purpose we use logic from before but via client.
    });
    // NOTE: apps.event.authorizations.list is typically for checking *specific* events.
    // However, if we just want to verify the token works, we run auth.test
    const authTest = await client.auth.test();

    const blocks = [
      { type: "header", text: { type: "plain_text", text: "🔐 App Authorization (Bolt)", emoji: true } },
      { type: "divider" },
      {
        type: "section",
        fields: [
          { type: "mrkdwn", text: `*Bot ID:*\n${authTest.bot_id}` },
          { type: "mrkdwn", text: `*User ID:*\n${authTest.user_id}` },
          { type: "mrkdwn", text: `*Team:*\n${authTest.team}` },
          { type: "mrkdwn", text: `*Mode:*\nBolt JS Framework` }
        ]
      }
    ];

    await respond({
      response_type: "ephemeral",
      blocks: blocks
    });

  } catch (e) {
    await respond({
      response_type: "ephemeral",
      text: `❌ Authorization Check Failed: ${e.message}`
    });
  }
}

async function updateRepairStatus(repairId, status, userId, env) {
  const completedAt = status === "completed" ? ", completed_at = datetime('now')" : "";
  await env.DB.prepare(`
    UPDATE repairs 
    SET status = ?, assigned_to = ? ${completedAt}
    WHERE id = ?
  `).bind(status, userId, repairId).run();
}

function getHelp() {
  return {
    response_type: "ephemeral",
    blocks: [
      { type: "header", text: { type: "plain_text", text: "🔧 Repair Commands (Bolt)", emoji: true } },
      {
        type: "section",
        text: {
          type: "mrkdwn",
          text: `
\`/repair list\` - Show active repairs
\`/repair stats\` - Today's progress & revenue
\`/repair add <device> "<desc>" <price> <priority>\` - Add repair
\`/repair auth\` - Check Bolt Auth
\`/repair help\` - This message

NOIZYLAB Assistant Enabled 🤖
          `.trim()
        }
      }
    ]
  };
}
