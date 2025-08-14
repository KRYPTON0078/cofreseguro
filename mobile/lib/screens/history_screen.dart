import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/api_client.dart';
import '../services/session.dart';

class HistoryScreen extends StatelessWidget {
  const HistoryScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final session = context.read<SessionState>();
    return FutureBuilder<List<dynamic>>(
      future: context.read<ApiClient>().history(session.token!),
      builder: (context, snap) {
        if (!snap.hasData) return const Center(child: CircularProgressIndicator());
        final items = snap.data!;
        return ListView.builder(
          itemCount: items.length,
          itemBuilder: (context, i) {
            final item = items[i] as Map<String, dynamic>;
            return ListTile(
              title: Text('${item['risk_level']} — ${item['risk_score']}'),
              subtitle: Text('${item['text_preview']}'),
            );
          },
        );
      },
    );
  }
}
