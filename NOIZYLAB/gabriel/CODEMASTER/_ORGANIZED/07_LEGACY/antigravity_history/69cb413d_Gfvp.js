/**
 * NOIZYLAB SLACK REPAIRS WORKER
 * ═══════════════════════════════════════════════════════════════════════════
 * Handles /repair commands, interactive buttons, and notifications
 * Part of MC96DIGIUNIVERSE - GORUNFREE x1000
 * ═══════════════════════════════════════════════════════════════════════════
 */

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // Health check
    if (url.pathname === '/health') {
      return new Response(JSON.stringify({ status: 'online', service: 'noizylab-repairs' }), {
        headers: { 'Content-Type': 'application/json' }
      });
    }

    // Slack commands
    if (url.pathname === '/slack/commands' && request.method === 'POST') {
      return handleSlashCommand(request, env);
    }

    // Slack interactive buttons
    if (url.pathname === '/slack/interactive' && request.method === 'POST') {
      return handleInteractive(request, env);
    }

    // API endpoints
    if (url.pathname === '/api/repairs' && request.method === 'GET') {
      return getRepairs(env);
    }

    if (url.pathname === '/api/repairs' && request.method === 'POST') {
      return createRepair(request, env);
    }

    return new Response('NOIZYLAB Repairs API - GORUNFREE x1000', { status: 200 });
  }
};

// ═══════════════════════════════════════════════════════════════════════════
// SLASH COMMAND HANDLER
// ═══════════════════════════════════════════════════════════════════════════

async function handleSlashCommand(request, env) {
  const formData = await request.formData();
  const command = formData.get('command');
  const text = formData.get('text') || '';
  const userId = formData.get('user_id');
  const userName = formData.get('user_name');

  const args = text.trim().split(' ');
  const subCommand = args[0]?.toLowerCase() || 'help';

  let response;

  switch (subCommand) {
    case 'list':
      response = await listRepairs(env);
      break;
    case 'stats':
      response = await getStats(env);
      break;
    case 'add':
      response = await addRepair(args.slice(1), userId, userName, env);
      break;
    case 'auth':
      response = await checkAuthorizations(env);
      break;
    case 'help':
    default:
      response = getHelp();
  }

  return new Response(JSON.stringify(response), {
    headers: { 'Content-Type': 'application/json' }
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// INTERACTIVE BUTTON HANDLER
// ═══════════════════════════════════════════════════════════════════════════

async function handleInteractive(request, env) {
  const formData = await request.formData();
  const payload = JSON.parse(formData.get('payload'));

  const action = payload.actions[0];
  const actionId = action.action_id;
  const repairId = action.value;
  const userId = payload.user.id;
  const userName = payload.user.username;

  let message;

  if (actionId === 'start_repair') {
    await updateRepairStatus(repairId, 'in_progress', userId, env);
    message = `🔧 <@${userId}> started repair #${repairId}`;
    await postToChannel(env, message);
  } else if (actionId === 'complete_repair') {
    await updateRepairStatus(repairId, 'completed', userId, env);
    message = `✅ <@${userId}> completed repair #${repairId}`;
    await postToChannel(env, message);
  }

  // Update the original message
  const updatedList = await listRepairs(env);
  return new Response(JSON.stringify(updatedList), {
    headers: { 'Content-Type': 'application/json' }
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// DATABASE OPERATIONS
// ═══════════════════════════════════════════════════════════════════════════

async function listRepairs(env) {
  const { results } = await env.DB.prepare(`
    SELECT * FROM repairs 
    WHERE status != 'completed' 
    ORDER BY priority DESC, created_at ASC
    LIMIT 20
  `).all();

  if (!results || results.length === 0) {
    return {
      response_type: 'ephemeral',
      text: '📋 No active repairs in queue. Nice work! 🎉'
    };
  }

  const blocks = [
    {
      type: 'header',
      text: { type: 'plain_text', text: '🔧 Active Repairs', emoji: true }
    },
    { type: 'divider' }
  ];

  for (const repair of results) {
    const statusEmoji = repair.status === 'in_progress' ? '🟡' : '⚪';
    const priorityEmoji = repair.priority >= 3 ? '🔴' : repair.priority === 2 ? '🟠' : '⚪';

    blocks.push({
      type: 'section',
      text: {
        type: 'mrkdwn',
        text: `${statusEmoji} *#${repair.id}* - ${repair.device_type}\n${priorityEmoji} ${repair.description}\n💰 $${repair.price || 0}`
      },
      accessory: {
        type: 'button',
        text: {
          type: 'plain_text',
          text: repair.status === 'in_progress' ? '✅ Complete' : '▶️ Start',
          emoji: true
        },
        action_id: repair.status === 'in_progress' ? 'complete_repair' : 'start_repair',
        value: String(repair.id),
        style: repair.status === 'in_progress' ? 'primary' : undefined
      }
    });
  }

  return {
    response_type: 'in_channel',
    blocks: blocks
  };
}

async function getStats(env) {
  const today = new Date().toISOString().split('T')[0];

  // Today's completed
  const { results: todayResults } = await env.DB.prepare(`
    SELECT COUNT(*) as count, SUM(price) as revenue
    FROM repairs 
    WHERE status = 'completed' 
    AND DATE(completed_at) = ?
  `).bind(today).all();

  // Total pending
  const { results: pendingResults } = await env.DB.prepare(`
    SELECT COUNT(*) as count FROM repairs WHERE status != 'completed'
  `).all();

  // Weekly stats
  const { results: weeklyResults } = await env.DB.prepare(`
    SELECT COUNT(*) as count, SUM(price) as revenue
    FROM repairs 
    WHERE status = 'completed' 
    AND completed_at >= datetime('now', '-7 days')
  `).all();

  const todayCount = todayResults[0]?.count || 0;
  const todayRevenue = todayResults[0]?.revenue || 0;
  const pendingCount = pendingResults[0]?.count || 0;
  const weeklyCount = weeklyResults[0]?.count || 0;
  const weeklyRevenue = weeklyResults[0]?.revenue || 0;

  const target = 12;
  const progress = Math.min(todayCount, target);
  const progressBar = '█'.repeat(progress) + '░'.repeat(target - progress);

  return {
    response_type: 'in_channel',
    blocks: [
      {
        type: 'header',
        text: { type: 'plain_text', text: '📊 Repair Stats', emoji: true }
      },
      { type: 'divider' },
      {
        type: 'section',
        text: {
          type: 'mrkdwn',
          text: `*Today's Progress:*\n🎯 ${todayCount}/${target} repairs\n[${progressBar}]\n💰 $${todayRevenue.toFixed(2)} revenue`
        }
      },
      {
        type: 'section',
        text: {
          type: 'mrkdwn',
          text: `*Queue:* ${pendingCount} repairs waiting\n*This Week:* ${weeklyCount} repairs | $${weeklyRevenue.toFixed(2)}`
        }
      },
      {
        type: 'context',
        elements: [
          { type: 'mrkdwn', text: `⚡ GORUNFREE x1000 | ${new Date().toLocaleString()}` }
        ]
      }
    ]
  };
}

async function addRepair(args, userId, userName, env) {
  // Parse: /repair add iPhone "Screen cracked" 150 2
  if (args.length < 2) {
    return {
      response_type: 'ephemeral',
      text: '❌ Usage: `/repair add <device> "<description>" [price] [priority 1-3]`'
    };
  }

  const device = args[0];
  const description = args.slice(1, -2).join(' ').replace(/"/g, '') || args[1];
  const price = parseFloat(args[args.length - 2]) || 0;
  const priority = parseInt(args[args.length - 1]) || 1;

  await env.DB.prepare(`
    INSERT INTO repairs (device_type, description, price, priority, status, created_by, created_at)
    VALUES (?, ?, ?, ?, 'pending', ?, datetime('now'))
  `).bind(device, description, price, priority, userName).run();

  // Notify channel
  await postToChannel(env, `📥 New repair added by <@${userId}>:\n*${device}* - ${description} | $${price}`);

  return {
    response_type: 'ephemeral',
    text: `✅ Repair added: ${device} - ${description}`
  };
}

async function updateRepairStatus(repairId, status, userId, env) {
  const completedAt = status === 'completed' ? ", completed_at = datetime('now')" : '';

  await env.DB.prepare(`
    UPDATE repairs 
    SET status = ?, assigned_to = ? ${completedAt}
    WHERE id = ?
  `).bind(status, userId, repairId).run();
}

function getHelp() {
  return {
    response_type: 'ephemeral',
    blocks: [
      {
        type: 'header',
        text: { type: 'plain_text', text: '🔧 Repair Commands', emoji: true }
      },
      {
        type: 'section',
        text: {
          type: 'mrkdwn',
          text: `
\`/repair list\` - Show active repairs
\`/repair stats\` - Today's progress & revenue
\`/repair add <device> "<desc>" <price> <priority>\` - Add repair
\`/repair help\` - This message

*Priority:* 1=Low, 2=Normal, 3=High

🎯 *Daily Target:* 12 repairs
⚡ GORUNFREE x1000
          `.trim()
        }
      }
    ]
  };
}

// ═══════════════════════════════════════════════════════════════════════════
// AUTH CHECKS (PHASE 14)
// ═══════════════════════════════════════════════════════════════════════════

async function checkAuthorizations(env) {
  if (!env.SLACK_APP_TOKEN) {
    return {
      response_type: 'ephemeral',
      text: '⚠️ `SLACK_APP_TOKEN` is not configured. Cannot check `authorizations:read`.'
    };
  }

  try {
    const response = await fetch('https://slack.com/api/apps.event.authorizations.list', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${env.SLACK_APP_TOKEN}`,
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });

    const data = await response.json();

    if (!data.ok) {
      return {
        response_type: 'ephemeral',
        text: `❌ Authorization Check Failed: ${data.error}`
      };
    }

    // Format with Block Kit
    const blocks = [
      {
        type: 'header',
        text: { type: 'plain_text', text: '🔐 App Authorizations', emoji: true }
      },
      { type: 'divider' }
    ];

    for (const auth of data.authorizations) {
      blocks.push({
        type: 'section',
        fields: [
          { type: 'mrkdwn', text: `*Team ID:*\n${auth.team_id}` },
          { type: 'mrkdwn', text: `*User ID:*\n${auth.user_id}` },
          { type: 'mrkdwn', text: `*Is Bot:*\n${auth.is_bot ? 'Yes' : 'No'}` },
          { type: 'mrkdwn', text: `*Enterprise:*\n${auth.enterprise_id || 'None'}` }
        ]
      });
    }

    return {
      response_type: 'ephemeral',
      blocks: blocks
    };

  } catch (e) {
    return {
      response_type: 'ephemeral',
      text: `❌ Error checking authorizations: ${e.message}`
    };
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// SLACK API HELPERS
// ═══════════════════════════════════════════════════════════════════════════

async function postToChannel(env, message, channel = '#repair-queue') {
  if (!env.SLACK_BOT_TOKEN) return;

  await fetch('https://slack.com/api/chat.postMessage', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${env.SLACK_BOT_TOKEN}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      channel: channel,
      text: message
    })
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// REST API ENDPOINTS
// ═══════════════════════════════════════════════════════════════════════════

async function getRepairs(env) {
  const { results } = await env.DB.prepare('SELECT * FROM repairs ORDER BY created_at DESC LIMIT 50').all();
  return new Response(JSON.stringify({ repairs: results }), {
    headers: { 'Content-Type': 'application/json' }
  });
}

async function createRepair(request, env) {
  const data = await request.json();

  await env.DB.prepare(`
    INSERT INTO repairs (device_type, description, price, priority, status, created_by, created_at)
    VALUES (?, ?, ?, ?, 'pending', ?, datetime('now'))
  `).bind(
    data.device_type,
    data.description,
    data.price || 0,
    data.priority || 1,
    data.created_by || 'api'
  ).run();

  return new Response(JSON.stringify({ success: true }), {
    headers: { 'Content-Type': 'application/json' }
  });
}
