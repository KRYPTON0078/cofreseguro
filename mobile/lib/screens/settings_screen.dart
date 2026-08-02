import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../l10n/app_strings.dart';
import '../services/api_client.dart';
import '../services/session.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});
  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  late final TextEditingController apiController;
  Map<String, dynamic>? behaviour;
  String? behaviourError;

  @override
  void initState() {
    super.initState();
    final session = context.read<SessionState>();
    apiController = TextEditingController(text: session.apiBase);
    _loadBehaviour();
  }

  Future<void> _loadBehaviour() async {
    final session = context.read<SessionState>();
    try {
      final data = await context.read<ApiClient>().behaviour(
            session.apiBase,
            session.token!,
          );
      if (mounted) setState(() => behaviour = data);
    } catch (e) {
      if (mounted) setState(() => behaviourError = e.toString());
    }
  }

  @override
  Widget build(BuildContext context) {
    final session = context.watch<SessionState>();
    final t = AppStrings(session.locale);
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        Text(t.settings, style: Theme.of(context).textTheme.titleLarge),
        const SizedBox(height: 12),
        TextField(
          controller: apiController,
          decoration: InputDecoration(
            labelText: t.apiBase,
            helperText: 'Android emulator: http://10.0.2.2:8080',
            border: const OutlineInputBorder(),
          ),
          onSubmitted: (v) => session.setApiBase(v),
        ),
        const SizedBox(height: 8),
        FilledButton(
          onPressed: () => session.setApiBase(apiController.text),
          child: Text(t.apiBase),
        ),
        const SizedBox(height: 16),
        ListTile(
          contentPadding: EdgeInsets.zero,
          title: Text(t.language),
          trailing: DropdownButton<String>(
            value: session.locale,
            items: const [
              DropdownMenuItem(value: 'en', child: Text('English')),
              DropdownMenuItem(value: 'pt', child: Text('Português')),
            ],
            onChanged: (v) {
              if (v != null) session.setLocale(v);
            },
          ),
        ),
        const Divider(),
        Text(t.behaviour, style: Theme.of(context).textTheme.titleMedium),
        if (behaviourError != null) Text(behaviourError!),
        if (behaviour != null) ...[
          Text('Score: ${behaviour!['risk_score']}'),
          Text('High-risk: ${behaviour!['high_risk_count']} / ${behaviour!['total_analyses']}'),
        ],
        const SizedBox(height: 24),
        OutlinedButton(
          onPressed: () => session.clear(),
          child: Text(t.signOut),
        ),
      ],
    );
  }
}
