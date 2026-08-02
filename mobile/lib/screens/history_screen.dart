import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../l10n/app_strings.dart';
import '../services/api_client.dart';
import '../services/session.dart';

class HistoryScreen extends StatefulWidget {
  const HistoryScreen({super.key});
  @override
  State<HistoryScreen> createState() => _HistoryScreenState();
}

class _HistoryScreenState extends State<HistoryScreen> {
  late Future<List<dynamic>> future;

  @override
  void initState() {
    super.initState();
    future = _load();
  }

  Future<List<dynamic>> _load() {
    final session = context.read<SessionState>();
    return context.read<ApiClient>().history(session.apiBase, session.token!);
  }

  @override
  Widget build(BuildContext context) {
    final t = AppStrings(context.watch<SessionState>().locale);
    return RefreshIndicator(
      onRefresh: () async => setState(() => future = _load()),
      child: FutureBuilder<List<dynamic>>(
        future: future,
        builder: (context, snap) {
          if (!snap.hasData) {
            return const Center(child: CircularProgressIndicator());
          }
          final items = snap.data!;
          if (items.isEmpty) {
            return ListView(children: [ListTile(title: Text(t.history))]);
          }
          return ListView.separated(
            itemCount: items.length,
            separatorBuilder: (_, __) => const Divider(height: 1),
            itemBuilder: (context, i) {
              final row = items[i] as Map<String, dynamic>;
              return ListTile(
                title: Text('${row['risk_level']} · ${row['risk_score']}'),
                subtitle: Text('${row['text_preview'] ?? ''}'),
                trailing: Text('${row['engine'] ?? ''}'),
              );
            },
          );
        },
      ),
    );
  }
}
