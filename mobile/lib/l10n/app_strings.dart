class AppStrings {
  AppStrings(this.locale);
  final String locale;
  bool get _pt => locale.startsWith('pt');

  String get appName => 'CofreSeguro';
  String get tagline =>
      _pt ? 'Escudo contra fraude de dinheiro móvel' : 'Mobile-money fraud shield';
  String get email => _pt ? 'Email' : 'Email';
  String get password => _pt ? 'Palavra-passe' : 'Password';
  String get signIn => _pt ? 'Entrar' : 'Sign in';
  String get signOut => _pt ? 'Sair' : 'Sign out';
  String get analyze => _pt ? 'Analisar' : 'Analyze';
  String get history => _pt ? 'Histórico' : 'History';
  String get tips => _pt ? 'Dicas' : 'Tips';
  String get settings => _pt ? 'Definições' : 'Settings';
  String get pasteSms =>
      _pt ? 'Cole a mensagem SMS suspeita' : 'Paste the suspicious SMS';
  String get checkRisk => _pt ? 'Verificar risco' : 'Check risk';
  String get pickImage => _pt ? 'Analisar imagem' : 'Analyze image';
  String get apiBase => _pt ? 'URL da API' : 'API base URL';
  String get language => _pt ? 'Idioma' : 'Language';
  String get behaviour => _pt ? 'Risco comportamental' : 'Behavioural risk';
  String get loginFailed => _pt ? 'Falha no login' : 'Login failed';
  String get risk => _pt ? 'Risco' : 'Risk';
  String get explanation => _pt ? 'Explicação' : 'Explanation';
  String get tip => _pt ? 'Dica' : 'Tip';
  String get demoHint =>
      _pt ? 'demo@cofreseguro.app / demo123!' : 'demo@cofreseguro.app / demo123!';
}
