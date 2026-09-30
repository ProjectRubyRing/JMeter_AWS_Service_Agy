# -*- coding: utf-8 -*-
"""
Script to generate the comprehensive Excel workbook:
'JMeter_AWS_Performance_Testing_and_JVM_Guide.xlsx'
Using Meiryo UI font and Monotone styling.
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_excel_workbook(output_filename="JMeter_AWS_Performance_Testing_and_JVM_Guide.xlsx"):
    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)

    # Styling Constants (Strictly Meiryo UI & Monotone Palette)
    FONT_NAME = "Meiryo UI"

    font_title = Font(name=FONT_NAME, size=16, bold=True, color="FFFFFF")
    font_subtitle = Font(name=FONT_NAME, size=11, bold=True, color="333333")
    font_sec_hdr = Font(name=FONT_NAME, size=11, bold=True, color="FFFFFF")
    font_tbl_hdr = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFF")
    font_tbl_subhdr = Font(name=FONT_NAME, size=9, bold=True, color="222222")
    
    font_data = Font(name=FONT_NAME, size=9, color="111111")
    font_data_bold = Font(name=FONT_NAME, size=9, bold=True, color="111111")
    font_data_code = Font(name=FONT_NAME, size=9, color="222222")
    font_data_warn = Font(name=FONT_NAME, size=9, bold=True, color="000000")
    font_note = Font(name=FONT_NAME, size=8, italic=True, color="555555")

    # Fills (Monotone)
    fill_title = PatternFill(start_color="1F2421", end_color="1F2421", fill_type="solid") # Deep Charcoal Black
    fill_sec_hdr = PatternFill(start_color="3E444A", end_color="3E444A", fill_type="solid") # Slate Charcoal
    fill_tbl_hdr = PatternFill(start_color="2C3035", end_color="2C3035", fill_type="solid") # Dark Charcoal
    fill_tbl_subhdr = PatternFill(start_color="D6D8DB", end_color="D6D8DB", fill_type="solid") # Light Slate Gray
    fill_zebra = PatternFill(start_color="F7F8F9", end_color="F7F8F9", fill_type="solid") # Very soft off-white/gray
    fill_white = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
    fill_highlight = PatternFill(start_color="E9ECEF", end_color="E9ECEF", fill_type="solid") # Accent gray
    fill_alert = PatternFill(start_color="CED4DA", end_color="CED4DA", fill_type="solid") # Alert gray (Monotone warning)

    # Borders
    thin_gray = Side(style="thin", color="D0D4D9")
    thick_dark = Side(style="medium", color="4A4D52")
    double_bottom = Side(style="double", color="333333")
    
    border_cell = Border(left=thin_gray, right=thin_gray, top=thin_gray, bottom=thin_gray)
    border_header = Border(left=thin_gray, right=thin_gray, top=thick_dark, bottom=thick_dark)
    border_summary = Border(left=thin_gray, right=thin_gray, top=thin_gray, bottom=double_bottom)

    # Alignments
    align_left = Alignment(horizontal="left", vertical="center", wrap_text=True)
    align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    align_right = Alignment(horizontal="right", vertical="center", wrap_text=True)
    align_top_left = Alignment(horizontal="left", vertical="top", wrap_text=True)
    align_top_center = Alignment(horizontal="center", vertical="top", wrap_text=True)

    def apply_sheet_defaults(ws):
        ws.views.sheetView[0].showGridLines = True

    # -------------------------------------------------------------------------
    # SHEET 1: 01_全体概要・アーキテクチャ
    # -------------------------------------------------------------------------
    ws1 = wb.create_sheet(title="01_全体概要・アーキテクチャ")
    apply_sheet_defaults(ws1)

    # Title Banner
    ws1.merge_cells("A1:G1")
    ws1["A1"] = "全体パフォーマンステスト（JMeter）におけるAWS可観測性（Observability）統合設計書"
    ws1["A1"].font = font_title
    ws1["A1"].fill = fill_title
    ws1["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws1.row_dimensions[1].height = 40

    ws1.merge_cells("A2:G2")
    ws1["A2"] = "■ 本書は、JMeterによるAPI負荷計測時に監視すべきAWSサービス指標、およびECS Fargate上のJBoss EAPのJVM/ヒープ監視手法を網羅した技術仕様・運用指針です。"
    ws1["A2"].font = font_subtitle
    ws1["A2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws1.row_dimensions[2].height = 25

    # Section 1: システム全体構成モデル
    ws1.merge_cells("A4:G4")
    ws1["A4"] = "1. 全体テストアーキテクチャとデータフロー"
    ws1["A4"].font = font_sec_hdr
    ws1["A4"].fill = fill_sec_hdr
    ws1["A4"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws1.row_dimensions[4].height = 26

    headers_s1_1 = ["階層 / コンポーネント", "採用AWSサービス / ソフトウェア", "主機能 / 役割", "パフォーマンステスト時の監視観点", "提供可観測性サービス", "通信プロトコル / 方式", "備考 / 設計注意事項"]
    for col_idx, h in enumerate(headers_s1_1, start=1):
        cell = ws1.cell(row=5, column=col_idx, value=h)
        cell.font = font_tbl_hdr
        cell.fill = fill_tbl_hdr
        cell.alignment = align_center
        cell.border = border_header
    ws1.row_dimensions[5].height = 28

    data_s1_1 = [
        ("負荷生成クライアント", "Apache JMeter (分散負荷構成)", "シナリオ実行、仮想ユーザー多重生成、HTTPリクエスト送信、クライアント計測", "レスポンスタイム(Elapsed Time)、スループット(TPS)、エラー率(Error %)、ネットワーク帯域飽和", "JMeter HTML Dashboard, Backend Listener", "HTTP/1.1, HTTP/2 (TLS)", "クライアント側のCPU/メモリ飽和による計測遅延に注意"),
        ("DNS / エッジ配信", "Amazon Route 53 / Amazon CloudFront", "名前解決、エッジSSL/TLS終端、静的キャッシュ配信、DDoS防御", "名前解決遅延、エッジキャッシュヒット率、エッジレイテンシ、5xxエラー率", "CloudWatch Metrics, CloudFront Logs", "HTTPS / Anycast DNS", "APIテスト時はCloudFrontキャッシュバイパス設定を要確認"),
        ("ロードバランサ", "Application Load Balancer (ALB)", "トラフィック分散、ターゲット死活監視、ヘッダーベースルーティング、SSL終端", "ターゲット応答時間(TargetResponseTime)、Active/New接続数、ELB 5xx(502/503/504)発生有無", "CloudWatch Metrics, Access Logs", "HTTP/1.1, HTTP/2, gRPC", "キャパシティ急増時はALBのプレウォーミング考慮が必要"),
        ("コンテナ実行基盤", "Amazon ECS on AWS Fargate", "サーバレスコンテナ管理、自動配置、タスク分離、仮想リソース割り当て", "タスク単位CPU/メモリ使用率、タスク数スケーリング挙動、ネットワークI/O、ストレージI/O", "CloudWatch Container Insights, ECS Metrics", "cgroup v2 (Linux)", "ホストOSへのアクセス不可。cgroupによる強制OOM Killer(137)監視が肝"),
        ("アプリケーション基盤", "Red Hat JBoss EAP (OpenJDK 17/21)", "Jakarta EE APサーバ、Undertow HTTPエンジン、IronJacamarコネクションプール", "JVMヒープメモリ使用率、GC停止時間(STW)、Undertowスレッド枯渇、JDBCプール待機", "CloudWatch Application Signals, ADOT, JMX", "Javaバイトコード, JMX, OTLP", "コンテナメモリ(cgroup)とJVMヒープは別物。内部監視が必須"),
        ("データベース基盤", "Amazon Aurora (PostgreSQL / MySQL)", "リレーショナルDB、高可用性共有ストレージ、分散リードレプリカ", "CPU使用率、アクティブセッション数(AAS)、コミット/読込レイテンシ、IOPS、デッドロック", "CloudWatch Metrics, Performance Insights", "PostgreSQL / MySQL Wire Protocol", "Performance InsightsでボトルネックSQLと待機イベント(Wait Event)を特定"),
        ("キャッシュ基盤", "Amazon ElastiCache for Redis", "インメモリKVS、セッションストア、クエリキャッシュ", "EngineCPUUtilization(シングルスレッド飽和)、メモリ断片化、Evictions(破棄数)、接続数", "CloudWatch Metrics", "Redis RESP Protocol", "Redisはシングルスレッド処理のためEngineCPUUtilizationを監視"),
        ("分散トレーシング基盤", "AWS X-Ray / AWS Distro for OpenTelemetry (ADOT)", "リクエスト追跡、サービスマップ自動生成、ボトルネック区間可視化", "E2Eレイテンシ内訳、スパン別所要時間(Undertow→EJB→JDBC)、例外・エラー発生箇所", "X-Ray Trace, Service Map", "OTLP (OpenTelemetry Protocol)", "Trace ID注入によるエンドツーエンドの遅延要因ピンポイント特定")
    ]

    for row_idx, row_data in enumerate(data_s1_1, start=6):
        fill_curr = fill_white if row_idx % 2 == 0 else fill_zebra
        for col_idx, val in enumerate(row_data, start=1):
            cell = ws1.cell(row=row_idx, column=col_idx, value=val)
            cell.font = font_data_bold if col_idx in [1, 2] else font_data
            cell.fill = fill_curr
            cell.border = border_cell
            cell.alignment = align_center if col_idx in [1, 5, 6] else align_left
        ws1.row_dimensions[row_idx].height = 36

    # Section 2: 監視の3本柱とAWSサービスのポジショニング
    start_row_s1_2 = len(data_s1_1) + 8
    ws1.merge_cells(f"A{start_row_s1_2}:G{start_row_s1_2}")
    ws1[f"A{start_row_s1_2}"] = "2. 可観測性（Observability）の3本柱とAWSサービスマッピング"
    ws1[f"A{start_row_s1_2}"].font = font_sec_hdr
    ws1[f"A{start_row_s1_2}"].fill = fill_sec_hdr
    ws1[f"A{start_row_s1_2}"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws1.row_dimensions[start_row_s1_2].height = 26

    headers_s1_2 = ["柱（Pillar）", "定義と役割", "対象AWSサービス", "JMeter負荷試験における重要性", "確認可能な主要項目", "長所・得意領域", "短所・注意点"]
    for col_idx, h in enumerate(headers_s1_2, start=1):
        cell = ws1.cell(row=start_row_s1_2+1, column=col_idx, value=h)
        cell.font = font_tbl_hdr
        cell.fill = fill_tbl_hdr
        cell.alignment = align_center
        cell.border = border_header
    ws1.row_dimensions[start_row_s1_2+1].height = 28

    data_s1_2 = [
        ("メトリクス\n(Metrics)", "数値時系列データ。システムの健康状態・負荷状況を俯瞰する集計値。", "Amazon CloudWatch Metrics\nCloudWatch Container Insights\nCloudWatch Application Signals", "全体キャパシティ評価、リソース飽和度検知、オートスケーリング動作確認の最重要指標。", "CPU使用率、メモリ使用量、ALB応答時間、リクエスト数、GC停止時間、DB接続数", "リアルタイム性、軽量、長期トレンド把握、アラーム設定が容易。", "個別の遅延リクエストの特定や、深い内部原因の調査には不向き。"),
        ("トレース\n(Traces)", "単一リクエストが複数分散コンポーネントを横断する際の実行経路と所要時間記録。", "AWS X-Ray\nAWS Distro for OpenTelemetry (ADOT)\nCloudWatch Application Signals", "JMeterで観測された「特定の遅いリクエスト」がシステム内部のどの処理で滞留したかを特定。", "E2E所要時間、Undertow処理時間、JDBCクエリ実行時間、外部API呼出時間、例外スタック", "区間別遅延の可視化、サービス依存関係図(Service Map)、ボトルネック特定。", "サンプリング設計が必要（100%取得はデータ量・コスト・オーバーヘッド増）。"),
        ("ログ\n(Logs)", "タイムスタンプ付きの離散的イベント記録。詳細なコンテキストと文脈情報。", "Amazon CloudWatch Logs\nCloudWatch Logs Insights\nAWS FireLens (Fluent Bit)", "エラー発生時のスタックトレース確認、JVM GC詳細ログ解析、Undertowアクセス詳細解析。", "GCポーズ時間詳細、Java例外ログ、JBossデプロイログ、Slow Queryログ", "極めて詳細な情報量、アドホックな集計クエリ(Logs Insights)が可能。", "データ量が膨大になりやすい、リアルタイムな俯瞰把握にはクエリ実行が必要。")
    ]

    for offset, row_data in enumerate(data_s1_2, start=2):
        r = start_row_s1_2 + offset
        fill_curr = fill_white if offset % 2 == 0 else fill_zebra
        for col_idx, val in enumerate(row_data, start=1):
            cell = ws1.cell(row=r, column=col_idx, value=val)
            cell.font = font_data_bold if col_idx == 1 else font_data
            cell.fill = fill_curr
            cell.border = border_cell
            cell.alignment = align_center if col_idx in [1, 3] else align_left
        ws1.row_dimensions[r].height = 55

    col_widths_s1 = [22, 28, 28, 32, 30, 24, 28]
    for i, w in enumerate(col_widths_s1, start=1):
        ws1.column_dimensions[get_column_letter(i)].width = w

    # -------------------------------------------------------------------------
    # SHEET 2: 02_AWSサービス別メトリクス一覧
    # -------------------------------------------------------------------------
    ws2 = wb.create_sheet(title="02_AWSサービス別メトリクス一覧")
    apply_sheet_defaults(ws2)

    ws2.merge_cells("A1:H1")
    ws2["A1"] = "JMeter API負荷計測時に確認すべきAWSサービス別メトリクス・トレース指標一覧"
    ws2["A1"].font = font_title
    ws2["A1"].fill = fill_title
    ws2["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws2.row_dimensions[1].height = 40

    headers_s2 = ["AWSサービス", "分類 / レイヤ", "メトリクス名 / 指標名", "単位 / 統計", "正常範囲の目安", "危険・警告の閾値", "指標の意味・パフォーマンス上の意義", "劣化時に疑うべき原因・調査アクション"]
    for col_idx, h in enumerate(headers_s2, start=1):
        cell = ws2.cell(row=3, column=col_idx, value=h)
        cell.font = font_tbl_hdr
        cell.fill = fill_tbl_hdr
        cell.alignment = align_center
        cell.border = border_header
    ws2.row_dimensions[3].height = 30

    metrics_data = [
        # ALB
        ("Application Load Balancer (ALB)", "レイテンシ", "TargetResponseTime", "Seconds (Average, p90, p99)", "< 0.5s (要件による)", "p99 > 1.0s または急上昇", "ターゲット(ECSタスク)がリクエストを受信してから応答を返すまでの処理時間。", "JBoss EAPのUndertowスレッド枯渇、JVMのFull GC発生、DBスロークエリを疑う。"),
        ("Application Load Balancer (ALB)", "トラフィック", "RequestCount", "Count (Sum)", "試験設計通りのTPS", "設計値と乖離 / 急減", "ALBがターゲットへルーティングした総リクエスト数。", "JMeter側の負荷生成能力不足、ネットワーク詰まり、または途中の4xx/5xx遮断。"),
        ("Application Load Balancer (ALB)", "接続管理", "ActiveConnectionCount", "Count (Sum/Average)", "安定推移", "際限なく増加", "クライアントからALB、およびALBからターゲットへのアクティブなTCP接続数。", "Keep-Alive接続の滞留、後続ECSタスクの応答遅延による接続詰まり。"),
        ("Application Load Balancer (ALB)", "接続管理", "NewConnectionCount", "Count (Sum)", "スループットと比例", "急増・乱高下", "1秒間または1分間に新しく確立されたTCP接続数。", "短時間での大量接続によるALBキャパシティ逼迫。Keep-Alive有効化を確認。"),
        ("Application Load Balancer (ALB)", "エラー(ターゲット)", "HTTPCode_Target_5XX_Count", "Count (Sum)", "0", "> 0", "ECS上のJBoss EAPが返却した5xxエラー(500, 502, 503等)。", "Javaアプリケーション内部でのUnhandled Exception、DB接続失敗、タイムアウト。"),
        ("Application Load Balancer (ALB)", "エラー(ELB自体)", "HTTPCode_ELB_5XX_Count", "Count (Sum)", "0", "> 0 (特に502, 504)", "ALB自体が生成したエラー。502=ターゲット切断、503=健全ターゲット不在、504=応答タイムアウト。", "ECSタスクのクラッシュ(OOMKilled)、ALBアイドルタイムアウト超過、タスク過負荷。"),
        ("Application Load Balancer (ALB)", "健全性", "UnHealthyHostCount", "Count (Average/Max)", "0", "> 0", "ALBヘルスチェックに失敗したターゲット(ECSタスク)の台数。", "ヘルスチェックURL応答遅延、JVMのStop-The-World、メモリ枯渇による応答不能。"),
        ("Application Load Balancer (ALB)", "インフラ", "RejectedConnectionCount", "Count (Sum)", "0", "> 0", "ALBの接続上限超過やサージキュー溢れにより拒否された接続数。", "ALBのキャパシティ不足。負荷試験前のプレウォーミング申請を検討。"),
        
        # Amazon ECS on Fargate
        ("Amazon ECS on Fargate", "CPU", "CpuUtilized / CPUUtilization", "Percent (%) (Average/Max)", "50% - 70%", "> 80% (継続)", "Fargateタスクに割り当てられたvCPUに対する実際のCPU使用率。", "Javaコンパイル負荷、高頻度のGC実行、非効率なループ処理、暗号化処理負荷。"),
        ("Amazon ECS on Fargate", "メモリ(cgroup)", "MemoryUtilized / MemoryUtilization", "Percent (%) / Bytes", "< 80%", "> 90% (OOM危険)", "コンテナcgroup全体のメモリ消費。JVMヒープ＋ネイティブ＋Metaspace＋OSバッファ。", "メモリリーク。100%に達するとFargateによりExit Code 137でプロセス強制終了。"),
        ("Amazon ECS on Fargate", "ネットワーク", "NetworkRxBytes / NetworkTxBytes", "Bytes/sec (Sum)", "ネットワーク上限以下", "急激なスパイク/頭打ち", "コンテナのネットワーク送受信バイト数。", "大量のクエリ結果取得、大きなペイロード返却によるFargate帯域制限到達。"),
        ("Amazon ECS on Fargate", "ストレージ", "StorageReadBytes / StorageWriteBytes", "Bytes/sec (Sum)", "低負荷", "過剰なI/O", "コンテナのローカルエフェメラルストレージへの読み書き量。", "過剰なアプリケーションログ出力、一時ファイルの大量書き込みによるディスクI/O遅延。"),

        # CloudWatch Application Signals (JVM / APM)
        ("CloudWatch Application Signals", "JVMヒープ", "jvm.memory.used (type=heap)", "Bytes (Average/Max)", "< Maxの70%", "> Maxの85% (継続)", "JVMのヒープ領域（Eden + Survivor + Old Gen）の実際の使用量。", "Javaヒープ枯渇、長期生存オブジェクトのリーク、不適切なキャッシュ蓄積。"),
        ("CloudWatch Application Signals", "JVM非ヒープ", "jvm.memory.used (type=non_heap)", "Bytes (Average/Max)", "安定推移", "右肩上がり増加", "Metaspace、Code Cache、Compressed Class Spaceの使用量。", "動的クラス生成リーク、JBossデプロイ残留、ネイティブメモリ肥大化。"),
        ("CloudWatch Application Signals", "JVM GC", "jvm.gc.duration", "Milliseconds (Sum/Max)", "< 50ms / 回", "> 200ms / 回 (STW)", "ガベージコレクションによってアプリケーションスレッドが完全停止した時間(STW)。", "G1GCのチューニング不足、Old領域枯渇によるFull GC発生、巨大オブジェクト割当。"),
        ("CloudWatch Application Signals", "JVMスレッド", "jvm.thread.count", "Count (Average/Max)", "安定推移", "上限値に張り付き", "JVM内のアクティブスレッド数（Undertowワーカースレッド、非同期タスク等）。", "DB接続待ちや外部API待ちによるUndertowリクエストスレッドの滞留・枯渇。"),
        ("CloudWatch Application Signals", "サービスレベル", "Latency (p50, p90, p99)", "Milliseconds", "SLO目標値以内", "SLO目標超過", "Application Signalsが自動計装により計測するサービス処理所要時間。", "ボトルネックオペレーションの特定、依存先サービス（DBや外部API）の遅延。"),

        # AWS X-Ray / ADOT Tracing
        ("AWS X-Ray / ADOT", "トレース", "Trace Duration (E2Eレイテンシ)", "Seconds / Milliseconds", "< 0.5s", "p95/p99の急増", "リクエスト開始から完了までの全体所要時間。サービスマップ上で色分け表示。", "トレース詳細を展開し、最も所要時間の長いサブセグメント(Subsegment)を特定。"),
        ("AWS X-Ray / ADOT", "トレース", "Subsegment Duration (Undertow/EJB)", "Milliseconds", "安定", "特定区間のみ遅延", "JBoss EAP内部のServlet実行、EJBビジネスロジック実行に要した時間。", "Javaコード内の非同期ロック競合、直列ループ処理、CPU高負荷による実行遅延。"),
        ("AWS X-Ray / ADOT", "トレース", "Subsegment Duration (JDBC/SQL)", "Milliseconds", "< 10ms (単一クエリ)", "> 100ms", "JBossからAurora/RDSに対するSQLクエリ実行および結果フェッチ所要時間。", "インデックス不足によるフルスキャン、テーブルロック待ち、DBバッファキャッシュミス。"),
        ("AWS X-Ray / ADOT", "エラー追跡", "FaultRate / ErrorRate", "Percent (%)", "0%", "> 0.1%", "HTTP 5xx (Fault) および HTTP 4xx (Error) の発生割合。", "X-RayトレースからHTTPステータス500のスタックトレースを抽出し即時原因分析。"),

        # Amazon Aurora / RDS
        ("Amazon Aurora / RDS", "CPU", "CPUUtilization", "Percent (%)", "< 60%", "> 80%", "データベースインスタンスのCPU使用率。", "非効率なSQLクエリ実行、同時実行セッション過多、集計処理の集中。"),
        ("Amazon Aurora / RDS", "メモリ", "FreeableMemory", "Bytes", "安定", "極小値に張り付き", "OSおよびDBエンジンが利用可能な空きメモリ量。", "ワークメモリ不足による一時テーブルのディスク書き出し発生。"),
        ("Amazon Aurora / RDS", "接続管理", "DatabaseConnections", "Count", "< プール上限", "最大接続数に到達", "データベースに対して現在開かれているアクティブな接続数。", "JBoss EAP側のデータソース接続リーク(Connection Leak)、プール設定不足。"),
        ("Amazon Aurora / RDS", "レイテンシ", "ReadLatency / WriteLatency", "Milliseconds", "< 5ms", "> 20ms", "ディスクストレージへの読み取り・書き込みに要する平均所要時間。", "AuroraストレージノードのI/O競合、分散ストレージへの負荷集中。"),
        ("Amazon Aurora / RDS", "待機イベント", "Performance Insights: AAS", "Sessions (Count)", "< vCPU数", "> vCPU数 (過負荷)", "平均アクティブセッション数(AAS)と待機イベント(Wait Event)内訳。", "CPU飽和(CPU)、行ロック待機(Lock:transaction)、I/O待機(io:datafileread)。"),

        # Amazon ElastiCache (Redis)
        ("Amazon ElastiCache", "CPU (コア)", "EngineCPUUtilization", "Percent (%)", "< 65%", "> 80%", "Redisメインスレッドを実行しているCPUコアの使用率(最重要)。", "キー設計の偏り、重いO(N)コマンド(KEYS, SMEMBERS等)の頻繁な実行。"),
        ("Amazon ElastiCache", "メモリ", "CurrConnections / Evictions", "Count / Count", "Evictions=0", "Evictions > 0", "現在のクライアント接続数、およびメモリ枯渇により破棄されたキー数。", "maxmemory超過によるキャッシュ強制追い出し。TTL設計やノードサイズ見直し。")
    ]

    for row_idx, row_data in enumerate(metrics_data, start=4):
        fill_curr = fill_white if row_idx % 2 == 0 else fill_zebra
        for col_idx, val in enumerate(row_data, start=1):
            cell = ws2.cell(row=row_idx, column=col_idx, value=val)
            cell.font = font_data_code if col_idx == 3 else (font_data_bold if col_idx in [1, 2] else font_data)
            cell.fill = fill_curr
            cell.border = border_cell
            cell.alignment = align_center if col_idx in [2, 4, 5, 6] else align_left
        ws2.row_dimensions[row_idx].height = 32

    col_widths_s2 = [26, 18, 30, 24, 20, 24, 38, 42]
    for i, w in enumerate(col_widths_s2, start=1):
        ws2.column_dimensions[get_column_letter(i)].width = w

    # -------------------------------------------------------------------------
    # SHEET 3: 03_JMeter計測時チェックシート
    # -------------------------------------------------------------------------
    ws3 = wb.create_sheet(title="03_JMeter計測時チェックシート")
    apply_sheet_defaults(ws3)

    ws3.merge_cells("A1:G1")
    ws3["A1"] = "JMeter API負荷テスト時のボトルネック特定相関チェックシート"
    ws3["A1"].font = font_title
    ws3["A1"].fill = fill_title
    ws3["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws3.row_dimensions[1].height = 40

    headers_s3 = ["JMeter側観測事象", "疑われる障害・ボトルネック", "最優先で確認すべきAWSメトリクス", "相関確認用トレース / ログ", "切り分け判定基準（Decision Criteria）", "根本原因（Root Cause）の典型例", "対策・チューニングアクション"]
    for col_idx, h in enumerate(headers_s3, start=1):
        cell = ws3.cell(row=3, column=col_idx, value=h)
        cell.font = font_tbl_hdr
        cell.fill = fill_tbl_hdr
        cell.alignment = align_center
        cell.border = border_header
    ws3.row_dimensions[3].height = 30

    check_data = [
        ("JMeterで平均・99%レスポンスタイムが線形に悪化するが、TPSは横ばい", "直列処理によるスレッド/コネクション枯渇、またはDB待ち", "ALB: TargetResponseTime\nECS: CPUUtilization\nRDS: DatabaseConnections, AAS", "X-Ray: サービスマップのJDBC区間所要時間\nCloudWatch: jvm.thread.count", "ALBのTargetResponseTimeも比例して上昇しており、かつECSのCPUは低い場合、バックエンド待ち。", "DB接続プール(IronJacamar)の上限到達、スロークエリによるロック待ち、外部API遅延。", "DBインデックス追加、データソースmax-pool-size拡大、Undertowスレッド数最適化。"),
        ("負荷上昇に伴い、JMeterでHTTP 502 Bad Gatewayが多発する", "ECS Fargateタスクの異常終了（クラッシュ/OOMKilled）", "ALB: HTTPCode_ELB_502_Count\nALB: UnHealthyHostCount\nECS: MemoryUtilized", "ECSイベントログ: Exit Code 137 (OOMKilled)\nCloudWatch Logs: OutOfMemoryError", "ALB 502急増と同時にUnHealthyHostCountが上昇し、ECSタスクが置換(再起動)されている。", "コンテナメモリ(cgroup)超過によるFargate OSからのSIGKILL(137)。JVMヒープ外リーク。", "Fargateタスクメモリ増量、-XX:MaxRAMPercentageの引き下げ(例: 70%→60%)、Metaspace制限。"),
        ("JMeterで定期的に数十秒スパイク状の遅延が発生し、その後復旧する", "JVMのFull GCによるStop-The-World (STW) 発生", "Signals: jvm.gc.duration\nSignals: jvm.memory.used (Old Gen)\nALB: TargetResponseTime", "CloudWatch Logs: GC詳細ログ (-Xlog:gc*)\nX-Ray: 全体レイテンシの周期的一斉遅延", "スパイク発生時刻と jvm.gc.duration の大停止時刻が秒単位で完全に一致する。", "G1GCのOld領域飽和、一時オブジェクトの大量生成(Allocation Failure)、ヒープサイジング不足。", "ヒープサイズ拡大、G1ReservePercent調整、InitiatingHeapOccupancyPercent引き下げ。"),
        ("負荷を上げてもJMeterのTPSが一定値で頭打ちになり、エラーも出ない", "ALBまたはECSスレッドプール、あるいはJMeterクライアント自体の限界", "ALB: ActiveConnectionCount\nALB: RejectedConnectionCount\nECS: CPUUtilization", "JMeterログ: JMeter実行端末のCPU/メモリ\nX-Ray: Undertowリクエストキューイング時間", "サーバ側リソース(CPU/メモリ/DB)に余裕があるのにTPSが上がらない。", "JMeterクライアントのCPU100%、ローカルポート枯渇、ALB未暖機、Undertowスレッド上限。", "JMeter負荷機の分散多重化、Keep-Alive設定見直し、ALBプレウォーミング申請。"),
        ("JMeterでHTTP 504 Gateway Timeoutが頻発する", "ALBのIdle Timeout設定超過、またはECS・DBのデッドロック", "ALB: HTTPCode_ELB_504_Count\nALB: TargetResponseTime\nRDS: Performance Insights (Lock:transaction)", "CloudWatch Logs: JBossスレッドダンプ (Thread Dump)\nX-Ray: 60秒以上停滞しているトレース", "TargetResponseTimeがALBのIdle Timeout値(デフォルト60s)に到達して切断されている。", "トランザクションのデッドロック、無限ループ、巨大ファイルの同期処理、外部API無応答。", "スレッドダンプ解析によるロック競合箇所の特定、ALBタイムアウト設計見直し、非同期化。"),
        ("特定のエンドポイントのみ極端にレスポンスが遅く、全体に波及する", "特定APIのスロークエリまたはN+1問題によるリソース独占", "Signals: Latency (Operation別)\nRDS: Performance Insights (Top SQL)", "X-Ray: 当該URLのトレース詳細（SQL発行回数が数百回に達している）", "Application Signalsのサービスマップで特定APIのみ赤色(高レイテンシ)表示される。", "JPA/HibernateのN+1クエリ、インデックスが効かない結合検索、不必要な全件SELECT。", "HibernateのFetch Join適用、バルク取得への変更、Redisキャッシュ導入によるオフロード。")
    ]

    for row_idx, row_data in enumerate(check_data, start=4):
        fill_curr = fill_white if row_idx % 2 == 0 else fill_zebra
        for col_idx, val in enumerate(row_data, start=1):
            cell = ws3.cell(row=row_idx, column=col_idx, value=val)
            cell.font = font_data_bold if col_idx == 1 else font_data
            cell.fill = fill_curr
            cell.border = border_cell
            cell.alignment = align_top_left if col_idx in [1, 2, 6, 7] else (align_top_center if col_idx == 5 else align_top_left)
        ws3.row_dimensions[row_idx].height = 55

    col_widths_s3 = [28, 26, 30, 30, 34, 34, 38]
    for i, w in enumerate(col_widths_s3, start=1):
        ws3.column_dimensions[get_column_letter(i)].width = w

    # -------------------------------------------------------------------------
    # SHEET 4: 04_Fargate_JBoss_JVM監視詳細
    # -------------------------------------------------------------------------
    ws4 = wb.create_sheet(title="04_Fargate_JBoss_JVM監視詳細")
    apply_sheet_defaults(ws4)

    ws4.merge_cells("A1:G1")
    ws4["A1"] = "ECS Fargate環境におけるJBoss EAPのJVM・ヒープメモリ監視設計"
    ws4["A1"].font = font_title
    ws4["A1"].fill = fill_title
    ws4["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws4.row_dimensions[1].height = 40

    # Section 1: なぜ標準ECSメトリクスだけではJVMヒープがわからないのか？
    ws4.merge_cells("A3:G3")
    ws4["A3"] = "1. コンテナメモリ（cgroup）とJVMヒープメモリの構造的相違点（最重要概念）"
    ws4["A3"].font = font_sec_hdr
    ws4["A3"].fill = fill_sec_hdr
    ws4["A3"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws4.row_dimensions[3].height = 26

    diff_headers = ["項目", "ECS標準メトリクス（cgroup Memory）", "JVM内部メモリ（Heap & Non-Heap）", "監視上の落とし穴・致命的リスク"]
    ws4.merge_cells("A4:B4")
    ws4["A4"] = diff_headers[0]
    ws4["C4"] = diff_headers[1]
    ws4["D4"] = diff_headers[2]
    ws4.merge_cells("E4:G4")
    ws4["E4"] = diff_headers[3]
    for col_char in ["A", "B", "C", "D", "E", "F", "G"]:
        c = ws4[f"{col_char}4"]
        c.font = font_tbl_hdr
        c.fill = fill_tbl_hdr
        c.alignment = align_center
        c.border = border_header
    ws4.row_dimensions[4].height = 26

    diff_data = [
        ("取得レイヤ・出所", "Linux OSのcgroup (memory.current / memory.usage_in_bytes)", "JVMプロセス内部 (JMX / OpenTelemetry Runtime Metrics)", "ECSメトリクスはOSから見た外枠しか見ておらず、JVM内部の状態は不可視。"),
        ("内包するメモリ領域", "JVM Heap + Metaspace + Thread Stack + CodeCache + DirectMemory + OSバッファ", "Heap (Eden, Survivor, Old Gen) および Non-Heap (Metaspace, CodeCache)", "ECSメモリが70%で安定していても、Old Genが100%になりFull GC地獄に陥っている事がある。"),
        ("OOM発生時の挙動", "cgroup制限超過時、LinuxカーネルのOOM Killerがプロセスを即座にSIGKILL (137)。", "ヒープ枯渇時、JVMが `java.lang.OutOfMemoryError: Java heap space` を送出。", "cgroup OOM時はヒープダンプを出力する猶予なくタスクが強制死するため原因調査不能。"),
        ("GC (ゴミ掃除) との連動", "GCが実行されてヒープ内のゴミが解放されても、OSには即座に返却されない（高止まり）。", "GC実行によってEden/Old領域の使用量がダイナミックに増減する。", "ECSメモリが90%に見えても、単にJVMがOSにメモリを返却していないだけの正常状態がある。")
    ]

    for row_idx, (d1, d2, d3, d4) in enumerate(diff_data, start=5):
        fill_curr = fill_white if row_idx % 2 == 0 else fill_zebra
        ws4.merge_cells(f"A{row_idx}:B{row_idx}")
        ws4[f"A{row_idx}"] = d1
        ws4[f"C{row_idx}"] = d2
        ws4[f"D{row_idx}"] = d3
        ws4.merge_cells(f"E{row_idx}:G{row_idx}")
        ws4[f"E{row_idx}"] = d4
        for col_char in ["A", "B", "C", "D", "E", "F", "G"]:
            c = ws4[f"{col_char}{row_idx}"]
            c.font = font_data_bold if col_char in ["A", "B"] else font_data
            c.fill = fill_curr
            c.border = border_cell
            c.alignment = align_center if col_char in ["A", "B"] else align_left
        ws4.row_dimensions[row_idx].height = 36

    # Section 2: JVM/ヒープ情報を取得・確認できるAWSサービスと実現手法
    ws4.merge_cells("A10:G10")
    ws4["A10"] = "2. JBoss EAPのJVM/ヒープ情報を可視化するAWSサービスと4つのアプローチ"
    ws4["A10"].font = font_sec_hdr
    ws4["A10"].fill = fill_sec_hdr
    ws4["A10"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws4.row_dimensions[10].height = 26

    approach_headers = ["アプローチ / 方式", "主要利用AWSサービス", "確認可能な具体的JVMメトリクス", "実装方式（アーキテクチャ）", "導入難易度", "オーバーヘッド", "総合推奨度・適用場面"]
    for col_idx, h in enumerate(approach_headers, start=1):
        cell = ws4.cell(row=11, column=col_idx, value=h)
        cell.font = font_tbl_hdr
        cell.fill = fill_tbl_hdr
        cell.alignment = align_center
        cell.border = border_header
    ws4.row_dimensions[11].height = 28

    approaches_data = [
        ("【方式1】\nCloudWatch\nApplication Signals\n(最新・推奨標準)", "Amazon CloudWatch\nApplication Signals\n(AWS X-Ray統合)", "・jvm.memory.used (Eden/Survivor/Old/Metaspace)\n・jvm.memory.limit / committed\n・jvm.gc.duration (STW停止時間)\n・jvm.thread.count (アクティブスレッド)", "JBossコンテナ起動引数に ADOT Java Agent (-javaagent:aws-opentelemetry-agent.jar) を追加。タスク定義でSignalsを有効化。", "低\n(コード改修不要、環境変数のみ)", "極めて低\n(< 1-2% CPU)", "★★★★★ (最推奨)\n2024-2026年のデファクト。自動計装でJVMメトリクスと分散トレース、SLOダッシュボードが一撃で手に入る。"),
        ("【方式2】\nContainer Insights\nwith Prometheus\n(JMX Exporter経由)", "CloudWatch Container Insights\n(Prometheus / EMF)\nAmazon Managed Prometheus", "・jvm_memory_bytes_used{area=heap}\n・jvm_gc_collection_seconds_sum\n・jboss_datasource_active_count\n・jboss_undertow_request_count", "JBossにjmx_prometheus_javaagentを組込み、Fargateタスク内にADOT Collectorサイドカーを配置してJMXエンドポイントをスクレイピング。", "中\n(サイドカー定義とYAML設定が必要)", "低\n(数秒毎の定期取得)", "★★★★☆\nJBoss固有のMBeans（DBコネクションプール数やUndertow統計）まで深く詳細に監視したい場合に最適。"),
        ("【方式3】\nCloudWatch Logs\nInsightsによる\nGCログ構造化解析", "Amazon CloudWatch Logs\nCloudWatch Logs Insights\nAWS FireLens (Fluent Bit)", "・Young GC / Full GC 発生頻度\n・GC前後のヒープ解放量\n・STW一時停止時間詳細\n・Humongous Allocation発生状況", "JVM引数に `-Xlog:gc*,gc+phases=debug:file=/var/log/gc.log` を指定。FireLens経由でCloudWatch Logsにリアルタイム転送しクエリ集計。", "低〜中\n(JVM引数設定とログ設計)", "極小\n(非同期ログ出力)", "★★★★☆\n負荷試験時のGC挙動をミリ秒単位で事後検証・根本原因分析する際の必須ツール。方式1と併用推奨。"),
        ("【方式4】\nECS Exec による\nリアルタイム\nCLI診断 (jcmd/CLI)", "Amazon ECS Exec\nAWS Systems Manager (SSM)", "・jcmd <pid> GC.heap_info (ヒープ詳細)\n・jcmd <pid> Thread.print (スレッドダンプ)\n・jboss-cli.sh (EAP MBean直接取得)", "aws ecs execute-command で稼働中Fargateコンテナに対話シェル接続し、JDK標準診断コマンドを実行。", "低\n(タスク定義でenableExecuteCommand有効化)", "実行時のみ一時的負荷", "★★★☆☆\n負荷試験中に特定タスクがハングした際、リアルタイムにスレッドダンプやヒープ内訳を緊急採取するデバッグ用途。")
    ]

    for row_idx, row_data in enumerate(approaches_data, start=12):
        fill_curr = fill_white if row_idx % 2 == 0 else fill_zebra
        for col_idx, val in enumerate(row_data, start=1):
            cell = ws4.cell(row=row_idx, column=col_idx, value=val)
            cell.font = font_data_bold if col_idx in [1, 7] else font_data
            cell.fill = fill_curr
            cell.border = border_cell
            cell.alignment = align_top_center if col_idx in [1, 5, 6] else align_top_left
        ws4.row_dimensions[row_idx].height = 68

    col_widths_s4 = [22, 24, 34, 36, 16, 16, 36]
    for i, w in enumerate(col_widths_s4, start=1):
        ws4.column_dimensions[get_column_letter(i)].width = w

    # -------------------------------------------------------------------------
    # SHEET 5: 05_動作原理と動作イメージ
    # -------------------------------------------------------------------------
    ws5 = wb.create_sheet(title="05_動作原理と動作イメージ")
    apply_sheet_defaults(ws5)

    ws5.merge_cells("A1:G1")
    ws5["A1"] = "可観測性データ収集の動作原理とランタイム実行イメージ"
    ws5["A1"].font = font_title
    ws5["A1"].fill = fill_title
    ws5["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws5.row_dimensions[1].height = 40

    # Section 1: データ収集パイプラインの動作原理
    ws5.merge_cells("A3:G3")
    ws5["A3"] = "1. エンドツーエンド・データ収集パイプラインの動作原理（Step-by-Step）"
    ws5["A3"].font = font_sec_hdr
    ws5["A3"].fill = fill_sec_hdr
    ws5["A3"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws5.row_dimensions[3].height = 26

    pipeline_headers = ["Step", "処理ステージ", "実行場所 / プロセス", "動作原理（Mechanism）", "生成・転送データ形式", "レイテンシ / 負荷への影響", "主要技術要素"]
    for col_idx, h in enumerate(pipeline_headers, start=1):
        cell = ws5.cell(row=4, column=col_idx, value=h)
        cell.font = font_tbl_hdr
        cell.fill = fill_tbl_hdr
        cell.alignment = align_center
        cell.border = border_header
    ws5.row_dimensions[4].height = 28

    pipeline_data = [
        ("Step 1", "リクエスト受信と\nTrace ID採番", "ALB (Application Load Balancer)", "クライアントからのHTTP要求を受信時、X-Amzn-Trace-Id ヘッダーの有無を確認。未設定ならALBが新規Trace IDを自動生成して後続へ伝搬。", "HTTP Request Header\n(X-Amzn-Trace-Id: Root=1-xxx)", "極小 (< 0.1ms)", "AWS ALB リバースプロキシ"),
        ("Step 2", "バイトコード自動計装\nとスパン生成", "JBoss EAP コンテナ\n(OpenJDK JVMプロセス)", "JVM起動時にADOT Java Agentがアタッチ。UndertowやJDBCのバイトコードを動的改変し、メソッド開始/終了を検知してSpanおよびJVMメトリクスをメモリ生成。", "OTLP Span / In-Memory Metric\n(Span: name, duration, tags)", "オーバーヘッド < 1-2%\n(非同期メモリキュー退避)", "Java Instrumentation API\nByteBuddy, OpenTelemetry"),
        ("Step 3", "ローカルプロセス間通信\n(サイドカー転送)", "Fargateタスク内部\n(localhost / UNIX Socket)", "アプリケーションコンテナ内のAgentから、同タスク内のADOT CollectorサイドカーコンテナへgRPC/OTLP (Port 4317) 経由で定期バッチ転送。", "OTLP / gRPC (Protocol Buffers)", "ゼロ（同一Fargateタスク内のローカルループバック通信）", "ECS Task Networking\n(awsvpc モード)"),
        ("Step 4", "メトリクス変換と\nAWS API送信", "ADOT Collector サイドカー\n(aws-otel-collector)", "受信したスパン/メトリクスをバッファリングし、AWS CloudWatch EMFおよびX-Ray APIフォーマットへ変換。IAMロール(SigV4)で署名しAWSエンドポイントへ非同期HTTPS送信。", "HTTPS POST (SigV4)\nCloudWatch EMF / X-Ray PutTraceSegments", "非同期バッチ送信のためアプリのレスポンスに影響なし", "AWS SDK, OpenTelemetry Collector\nEMF Exporter, X-Ray Exporter"),
        ("Step 5", "時系列集計と\n可視化・アラーム", "AWS CloudWatch バックエンド\nAWS X-Ray バックエンド", "CloudWatchが高解像度メトリクス(1秒/1分)として集計保存。X-RayがTrace IDを突合してサービスマップと分散トレースツリーを動的生成。ダッシュボードに即時反映。", "時系列データベース (Time Series DB)\nX-Ray Trace Graph Database", "リアルタイム反映 (数秒〜1分以内)", "Amazon CloudWatch\nApplication Signals / X-Ray")
    ]

    for row_idx, row_data in enumerate(pipeline_data, start=5):
        fill_curr = fill_white if row_idx % 2 == 0 else fill_zebra
        for col_idx, val in enumerate(row_data, start=1):
            cell = ws5.cell(row=row_idx, column=col_idx, value=val)
            cell.font = font_data_bold if col_idx in [1, 2] else font_data
            cell.fill = fill_curr
            cell.border = border_cell
            cell.alignment = align_center if col_idx in [1, 2, 6] else align_left
        ws5.row_dimensions[row_idx].height = 42

    # Section 2: JVMヒープメモリとGCの動作メカニズム
    ws5.merge_cells("A11:G11")
    ws5["A11"] = "2. JVMヒープメモリ領域の構造とGC（Garbage Collection）動作メカニズム"
    ws5["A11"].font = font_sec_hdr
    ws5["A11"].fill = fill_sec_hdr
    ws5["A11"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws5.row_dimensions[11].height = 26

    jvm_headers = ["ヒープ領域 / 分類", "役割とライフサイクル", "GCアルゴリズムの挙動 (G1GC想定)", "滞留・枯渇時の症状", "最適化・監視の急所", "推奨JVMオプション"]
    ws5.cell(row=12, column=1, value=jvm_headers[0]).alignment = align_center
    ws5.cell(row=12, column=2, value=jvm_headers[1]).alignment = align_center
    ws5.cell(row=12, column=3, value=jvm_headers[2]).alignment = align_center
    ws5.cell(row=12, column=4, value=jvm_headers[3]).alignment = align_center
    ws5.cell(row=12, column=5, value=jvm_headers[4]).alignment = align_center
    ws5.merge_cells("F12:G12")
    ws5.cell(row=12, column=6, value=jvm_headers[5]).alignment = align_center
    for c_idx in range(1, 8):
        cell = ws5.cell(row=12, column=c_idx)
        cell.font = font_tbl_hdr
        cell.fill = fill_tbl_hdr
        cell.border = border_header
    ws5.row_dimensions[12].height = 28

    jvm_data = [
        ("Young Generation:\nEden領域", "新規作成されたJavaオブジェクトが最初に割り当てられる領域。リクエスト毎のDTOや一時文字列。", "オブジェクト生成でEdenが満杯になると「Minor GC (Young GC)」が発動。生存オブジェクトのみSurvivorへコピー。", "過剰なリクエスト集中時に短時間で満杯になり、Young GC頻度が急増。CPU使用率上昇。", "アロケーション速度(MB/s)の監視。短命オブジェクトの速やかな破棄。", "-XX:+UseG1GC\n-XX:G1NewSizePercent=30"),
        ("Young Generation:\nSurvivor領域 (S0/S1)", "Minor GCを生き残ったオブジェクトが一時滞在する領域。FromとToの2面を交互に使用。", "GC毎にエイジ(Age)がインクリメントされ、閾値(MaxTenuringThreshold)を超えるとOldへ昇格(Promotion)。", "Survivor領域が小さすぎると、短命オブジェクトがOld領域へ早期昇格(Premature Promotion)してしまう。", "Survivor境界の溢れ検知。Tenuring分布のログ確認。", "-XX:SurvivorRatio=8\n-XX:MaxTenuringThreshold=15"),
        ("Old Generation:\n(Tenured領域)", "長期生存オブジェクト（キャッシュ、シングルトンBean、JBossセッション、DBプール）が滞在。", "ヒープ使用率がIHOP (デフォルト45%) を超えると、バックグラウンドで「Concurrent Marking」を開始。", "Old領域がゴミで満杯になると、全スレッドを停止させる壊滅的な「Full GC」が発生。", "最も監視すべき領域。右肩上がりの場合は確実にメモリリーク。", "-XX:InitiatingHeapOccupancyPercent=45\n-XX:G1ReservePercent=15"),
        ("Non-Heap:\nMetaspace", "クラス定義、メソッドメタデータ、定数プールを格納するネイティブメモリ領域（Java 8以降）。", "Full GC時または明示的なクリーンアップ時に不要なClassLoaderとともに解放される。", "動的クラス生成ライブラリのリーク等で肥大化。上限なしだとFargateのcgroupメモリを食い潰す。", "MaxMetaspaceSizeを設定し、cgroup OOM Killer(137)より前にJava例外で検知させる。", "-XX:MetaspaceSize=128m\n-XX:MaxMetaspaceSize=512m"),
        ("Non-Heap:\nDirect Memory / Buffers", "NIO(Netty, Undertow)がゼロコピー通信で使用するJVM外のダイレクトバッファ。", "GCとは直接連動せず、明示的な解放またはCleanerによる遅延解放。", "高負荷時にDirect Memoryがリークすると、ヒープには空きがあるのにcgroup OOMでコンテナ即死。", "Undertowのバッファプール設定およびDirectMemorySizeの制限。", "-XX:MaxDirectMemorySize=512m\n-XX:+UseContainerSupport")
    ]

    for row_idx, (j1, j2, j3, j4, j5, j6) in enumerate(jvm_data, start=13):
        fill_curr = fill_white if row_idx % 2 == 0 else fill_zebra
        ws5.cell(row=row_idx, column=1, value=j1).alignment = align_center
        ws5.cell(row=row_idx, column=2, value=j2).alignment = align_left
        ws5.cell(row=row_idx, column=3, value=j3).alignment = align_left
        ws5.cell(row=row_idx, column=4, value=j4).alignment = align_left
        ws5.cell(row=row_idx, column=5, value=j5).alignment = align_left
        ws5.merge_cells(f"F{row_idx}:G{row_idx}")
        ws5.cell(row=row_idx, column=6, value=j6).alignment = align_left
        for c_idx in range(1, 8):
            cell = ws5.cell(row=row_idx, column=c_idx)
            cell.font = font_data_code if c_idx in [1, 6, 7] else font_data
            cell.fill = fill_curr
            cell.border = border_cell
        ws5.row_dimensions[row_idx].height = 48

    col_widths_s5 = [20, 26, 32, 34, 30, 24, 24]
    for i, w in enumerate(col_widths_s5, start=1):
        ws5.column_dimensions[get_column_letter(i)].width = w

    # -------------------------------------------------------------------------
    # SHEET 6: 06_歴史的背景と進化の経緯
    # -------------------------------------------------------------------------
    ws6 = wb.create_sheet(title="06_歴史的背景と進化の経緯")
    apply_sheet_defaults(ws6)

    ws6.merge_cells("A1:G1")
    ws6["A1"] = "Java監視・AWSインフラ監視の歴史的変遷と現代の必要性"
    ws6["A1"].font = font_title
    ws6["A1"].fill = fill_title
    ws6["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws6.row_dimensions[1].height = 40

    headers_s6 = ["時代 / 年代", "実行環境モデル", "JBoss / Javaの特徴", "当時の監視手法とツール", "発生していた技術課題・ペイン（なぜ困ったか）", "次世代への進化の原動力（必要になった経緯）", "現代（2026年）への教訓"]
    for col_idx, h in enumerate(headers_s6, start=1):
        cell = ws6.cell(row=3, column=col_idx, value=h)
        cell.font = font_tbl_hdr
        cell.fill = fill_tbl_hdr
        cell.alignment = align_center
        cell.border = border_header
    ws6.row_dimensions[3].height = 30

    history_data = [
        ("第1世代\n(1990年代後半\n〜2000年代)", "オンプレミス物理サーバ\n(Bare Metal)", "JBoss AS 3/4/5\nJava 1.4 / Java 5 / 6\nモノリシック巨大構成", "・SNMPによるOS監視\n・JConsole / VisualVM (RMI接続)\n・運用者がSSHログインしてtopコマンド", "・物理IP固定前提のため動的変化に対応不能\n・RMIポート(1099, 9999)のファイアウォール開放が必要\n・負荷試験中にJConsoleを繋ぐとRMI自体が高負荷でサーバ停止", "クラウド化と仮想化の波。ハードウェア保守からの脱却と、インフラリソースの柔軟なプロビジョニング要求。", "JVM内部をネットワーク越しに直接デバッグする手法(RMI)は脆弱でスケーラビリティがない。"),
        ("第2世代\n(2006年\n〜2014年頃)", "クラウド仮想マシン\n(AWS EC2)", "JBoss EAP 6\nJava 7 / 8\n巨大VMインスタンス", "・CloudWatch基本メトリクス(CPU, Disk)\n・EC2 OS内 CloudWatch Logs Agent\n・JMX-Console, Zabbixエージェント", "・ハイパーバイザー監視のため「OSメモリ」がCloudWatchから見えない\n・オートスケーリングでIPが変わるとJMX監視が切断\n・分散した複数インスタンスのログ突合が困難", "コンテナ技術(Docker)の台頭。環境のポータビリティ向上と、ミリ秒単位での超高速デプロイ・軽量化要求。", "インフラの外側監視（ハイパーバイザー）だけでは、OSやJavaのメモリ枯渇に気づけない。"),
        ("第3世代\n(2015年\n〜2018年頃)", "コンテナ黎明期\n(Docker on EC2, ECS)", "JBoss EAP 7\nJava 8 (初期)\nコンテナ化の第一歩", "・Docker Stats, cgroup監視\n・Prometheus + JMX Exporter\n・ELK Stack (Elasticsearch, Logstash)", "【大問題】Java 8初期はcgroup未対応！ホストの物理メモリ(例:64GB)を認識し、コンテナ制限(2GB)を無視して巨大ヒープを確保し即死(OOMKilled)。", "OpenJDKのコンテナ認識機能(-XX:+UseContainerSupport, Java 8u191/Java 10)実装と、完全サーバレスコンテナの希求。", "コンテナ化する際は、ランタイム(JVM)がコンテナの境界(cgroup)を認識しているかが死活問題となる。"),
        ("第4世代\n(2018年\n〜2022年頃)", "サーバレスコンテナ\n(AWS ECS Fargate)", "JBoss EAP 7.3/7.4\nOpenJDK 11/17\nマイクロサービス化", "・CloudWatch Container Insights\n・AWS X-Ray SDK (独自計装)\n・FireLens (Fluent Bit) ログ転送", "・FargateはホストOSにSSH不可！従来のOSエージェントが一切動かない\n・一時的タスク(Ephemeral)のためIP追跡不能\n・X-Ray SDKの手動コード埋め込み改修が高コスト", "標準化された可観測性規格(OpenTelemetry)の策定と、コード改修不要の自動計装(Auto-Instrumentation)要求。", "サーバレス環境では「外部からのアクセス不可」が前提。アプリケーション自身がメトリクスを押し出す(Push型)設計が必須。"),
        ("第5世代\n(2023年\n〜2026年現代)", "マネージド可観測性\n(CloudWatch App Signals\n& OpenTelemetry標準)", "JBoss EAP 8\nOpenJDK 17 / 21\nクラウドネイティブ Jakarta EE", "・CloudWatch Application Signals\n・AWS Distro for OpenTelemetry (ADOT)\n・サービスマップ、SLO自動追跡", "・解決済：コード改修ゼロでJVMヒープ/GCと分散トレースを統合収集\n・課題：大量データ転送時のコスト管理と、サンプリングレートの最適化設計", "OpenTelemetryによるベンダーロックイン排除と、AIを活用した異常検知・根本原因自動特定(AIOps)。", "メトリクス・トレース・ログをバラバラに見る時代は終了。1つのTrace IDで全レイヤを串刺し分析するのが新標準。")
    ]

    for row_idx, row_data in enumerate(history_data, start=4):
        fill_curr = fill_white if row_idx % 2 == 0 else fill_zebra
        for col_idx, val in enumerate(row_data, start=1):
            cell = ws6.cell(row=row_idx, column=col_idx, value=val)
            cell.font = font_data_bold if col_idx in [1, 2] else font_data
            cell.fill = fill_curr
            cell.border = border_cell
            cell.alignment = align_top_center if col_idx in [1, 2] else align_top_left
        ws6.row_dimensions[row_idx].height = 55

    col_widths_s6 = [18, 24, 24, 28, 38, 38, 38]
    for i, w in enumerate(col_widths_s6, start=1):
        ws6.column_dimensions[get_column_letter(i)].width = w

    # -------------------------------------------------------------------------
    # SHEET 7: 07_小学生でもわかる図解解説
    # -------------------------------------------------------------------------
    ws7 = wb.create_sheet(title="07_小学生でもわかる図解解説")
    apply_sheet_defaults(ws7)

    ws7.merge_cells("A1:G1")
    ws7["A1"] = "【たとえ話で完全理解】巨大な遊園地とロボット執事の物語"
    ws7["A1"].font = font_title
    ws7["A1"].fill = fill_title
    ws7["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws7.row_dimensions[1].height = 40

    ws7.merge_cells("A3:G3")
    ws7["A3"] = "1. 登場人物と現実のITシステムの対応表"
    ws7["A3"].font = font_sec_hdr
    ws7["A3"].fill = fill_sec_hdr
    ws7["A3"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws7.row_dimensions[3].height = 26

    metaphor_headers = ["物語のキャラクター / アイテム", "実際のITシステム", "どんな役割？（たとえ話）", "実際のシステムの役割"]
    ws7.merge_cells("A4:B4")
    ws7["A4"] = metaphor_headers[0]
    ws7["C4"] = metaphor_headers[1]
    ws7.merge_cells("D4:E4")
    ws7["D4"] = metaphor_headers[2]
    ws7.merge_cells("F4:G4")
    ws7["F4"] = metaphor_headers[3]
    for col_char in ["A", "B", "C", "D", "E", "F", "G"]:
        c = ws7[f"{col_char}4"]
        c.font = font_tbl_hdr
        c.fill = fill_tbl_hdr
        c.alignment = align_center
        c.border = border_header
    ws7.row_dimensions[4].height = 26

    metaphor_data = [
        ("巨大バスツアー会社", "Apache JMeter", "1秒間に1000人の小学生を遊園地へ送り込んで「全員楽しく遊べるか？」を試す実験会社。", "APIに対して大量のリクエストを同時に送りつけ、性能や耐久性をテストする負荷測定ツール。"),
        ("遊園地の入場ゲートと\n交通整理のお巡りさん", "Application Load Balancer\n(ALB)", "やってきた小学生たちを、空いているアトラクションの小屋へ公平に案内する親切なお巡りさん。", "大量のWebリクエストを受け取り、稼働中の複数のコンテナ(ECSタスク)へバランス良く振り分ける装置。"),
        ("魔法のテント小屋", "Amazon ECS on Fargate\n(コンテナ実行基盤)", "草むしりや電気代を気にせず、必要な時だけポンと現れて用が済んだら消える便利なテント。", "サーバの面倒（OS管理やハード管理）を一切見なくて良い、サーバレスなコンテナ置き場。"),
        ("テントの中のロボット執事", "JBoss EAP\n(Javaアプリケーションサーバ)", "テントの中で、小学生から頼まれた注文（チケット発行や計算）を猛スピードで処理する優秀なロボット。", "ビジネスロジックを実行し、データベースとやり取りしてレスポンスを生成するミドルウェア。"),
        ("ロボットの頭脳・OS", "JVM (Java Virtual Machine)", "ロボット執事の頭の中で動いている特別なコンピュータOS。", "Javaプログラムを実行するための仮想マシン環境。メモリやスレッドを統括管理する。"),
        ("ロボットの作業デスク\n（机の広さ）", "ヒープメモリ (Heap Memory)", "ロボットが書類を広げて作業する机。机の広さには限界がある！", "Javaプログラムが実行中にデータやオブジェクトを一時的に置いておくメモリ領域。"),
        ("部屋のお掃除当番\n（ゴミ捨てタイム）", "ガベージコレクション (GC)\n(Garbage Collection)", "机が使わなくなった紙くずでいっぱいになった時、一斉にゴミ箱へ捨てるお掃除の時間。※掃除中はロボットが固まる！", "不要になったメモリ領域を自動で解放する仕組み。実行中(STW)はアプリの応答が一時停止する。"),
        ("魔法の透視カメラと\n光るバッジ", "AWS X-Ray / ADOT\n(分散トレーシング)", "小学生の服に光るバッジをつけて、入場ゲートからテント、宝物庫まで「どこで何分待たされたか」を丸見えにするカメラ。", "リクエストにTrace IDを付与し、ALB→JBoss→DBのどこで何ミリ秒かかったかを可視化するツール。")
    ]

    for row_idx, (m1, m2, m3, m4) in enumerate(metaphor_data, start=5):
        fill_curr = fill_white if row_idx % 2 == 0 else fill_zebra
        ws7.merge_cells(f"A{row_idx}:B{row_idx}")
        ws7[f"A{row_idx}"] = m1
        ws7[f"C{row_idx}"] = m2
        ws7.merge_cells(f"D{row_idx}:E{row_idx}")
        ws7[f"D{row_idx}"] = m3
        ws7.merge_cells(f"F{row_idx}:G{row_idx}")
        ws7[f"F{row_idx}"] = m4
        for col_char in ["A", "B", "C", "D", "E", "F", "G"]:
            c = ws7[f"{col_char}{row_idx}"]
            c.font = font_data_bold if col_char in ["A", "B", "C"] else font_data
            c.fill = fill_curr
            c.border = border_cell
            c.alignment = align_center if col_char in ["A", "B", "C"] else align_left
        ws7.row_dimensions[row_idx].height = 42

    # Section 2: 小学生の疑問に答えるQ&A
    start_row_s7_2 = len(metaphor_data) + 7
    ws7.merge_cells(f"A{start_row_s7_2}:G{start_row_s7_2}")
    ws7[f"A{start_row_s7_2}"] = "2. 子どもでもスッキリ納得！よくある疑問Q&A"
    ws7[f"A{start_row_s7_2}"].font = font_sec_hdr
    ws7[f"A{start_row_s7_2}"].fill = fill_sec_hdr
    ws7[f"A{start_row_s7_2}"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws7.row_dimensions[start_row_s7_2].height = 26

    qa_headers = ["質問（小学生の疑問）", "かんたんな答え", "くわしい技術の理由（なぜそうなるの？）"]
    ws7.merge_cells(f"A{start_row_s7_2+1}:B{start_row_s7_2+1}")
    ws7[f"A{start_row_s7_2+1}"] = qa_headers[0]
    ws7.merge_cells(f"C{start_row_s7_2+1}:D{start_row_s7_2+1}")
    ws7[f"C{start_row_s7_2+1}"] = qa_headers[1]
    ws7.merge_cells(f"E{start_row_s7_2+1}:G{start_row_s7_2+1}")
    ws7[f"E{start_row_s7_2+1}"] = qa_headers[2]
    for col_char in ["A", "B", "C", "D", "E", "F", "G"]:
        c = ws7[f"{col_char}{start_row_s7_2+1}"]
        c.font = font_tbl_hdr
        c.fill = fill_tbl_hdr
        c.alignment = align_center
        c.border = border_header
    ws7.row_dimensions[start_row_s7_2+1].height = 26

    qa_data = [
        ("Q1: なんでテントの外から体重計を見るだけじゃダメなの？\n（コンテナメモリとヒープメモリのちがい）", "テント全体の重さを見ても、ロボットの机の上がゴミだらけかどうかは外から見えないから！", "ECSのメモリ監視はOS全体のメモリを見ています。でもロボット(JVM)は、一度確保したメモリをOSになかなか返さない癖があります。だから外から見ると『90%使っている』ように見えても、机の中身(ヒープ)は掃除が終わってスカスカなこともあれば、逆に外からは普通に見えて机の上が満杯でパンク寸前のこともあるからです。"),
        ("Q2: お掃除の時間（GC）になると、なんでみんな待たされるの？\n（Stop The Worldってなに？）", "ロボットがお掃除している最中に書類を動かされると、どれがゴミかわからなくなって大混乱するから！", "JVMがメモリ掃除をする時、動いているプログラムが勝手にメモリを書き換えると危険なので、一瞬だけすべての動きをピタッと止めます。これを『Stop The World (STW)』と呼びます。普段は0.01秒で終わるから気づきませんが、ゴミが多すぎると何秒も止まってしまい、JMeterで測っている人たちは『急に返事が来なくなった！』と大騒ぎになります。"),
        ("Q3: なんで昔みたいにロボットの部屋へ直接見に行っちゃダメなの？\n（FargateでSSHができない理由）", "魔法のテント(Fargate)は『安全のため、外から勝手にドアを開けて入っちゃダメ』というルールだから！", "昔のサーバは人間がカギ(SSH)を使って中に入り、ロボットの様子を直接見られました。でもFargateはセキュリティを高めて管理を全自動にするため、人間が勝手に入れない仕組みになっています。その代わり、ロボット自身が『今机はこれくらい使ってるよ！』と手紙(CloudWatch Application SignalsやADOT)を書いて外のポストに届ける仕組みに進化しました。"),
        ("Q4: テントの制限体重を超えるとどうなっちゃうの？\n（OOM Killer Exit Code 137の恐怖）", "見張りの巨人(Linux OS)がやってきて、テントごと一瞬でペシャンコに壊してロボットをクビにしちゃいます！", "Fargateに設定したメモリ上限(例: 4GB)を1バイトでも超えると、OSの『OOM Killer』という非常停止装置が発動し、プロセスにSIGKILL(シグナル137)を撃ち込んで強制終了させます。遺言(エラーログ)を残す暇もなく即死するため、ロボットが悲鳴をあげる前にCloudWatchでヒープを監視して防ぐ必要があります。")
    ]

    for offset, (q1, q2, q3) in enumerate(qa_data, start=2):
        r = start_row_s7_2 + offset
        fill_curr = fill_white if offset % 2 == 0 else fill_zebra
        ws7.merge_cells(f"A{r}:B{r}")
        ws7[f"A{r}"] = q1
        ws7.merge_cells(f"C{r}:D{r}")
        ws7[f"C{r}"] = q2
        ws7.merge_cells(f"E{r}:G{r}")
        ws7[f"E{r}"] = q3
        for col_char in ["A", "B", "C", "D", "E", "F", "G"]:
            c = ws7[f"{col_char}{r}"]
            c.font = font_data_bold if col_char in ["A", "B"] else font_data
            c.fill = fill_curr
            c.border = border_cell
            c.alignment = align_top_left
        ws7.row_dimensions[r].height = 65

    col_widths_s7 = [22, 22, 28, 28, 30, 30, 30]
    for i, w in enumerate(col_widths_s7, start=1):
        ws7.column_dimensions[get_column_letter(i)].width = w

    # Freeze Panes for easy navigation
    ws1.freeze_panes = "A6"
    ws2.freeze_panes = "A4"
    ws3.freeze_panes = "A4"
    ws4.freeze_panes = "A5"
    ws5.freeze_panes = "A5"
    ws6.freeze_panes = "A4"
    ws7.freeze_panes = "A5"

    # Save workbook
    wb.save(output_filename)
    print(f"Successfully generated: {output_filename}")

if __name__ == "__main__":
    build_excel_workbook()
