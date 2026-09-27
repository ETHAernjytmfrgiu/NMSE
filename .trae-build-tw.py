import json
import opencc

SRC = 'Resources/ui/lang/zh-CN2.json'
OUT = 'Resources/ui/lang/zh-TW.json'

# "Galaxy" (銀河系) is a distinct concept from the star system (星系) in this editor
GALAXY_KEYS = {
    'discovery.col_galaxy', 'discovery.galaxy', 'exocraft.station_galaxy',
    'player.galaxy', 'player.galaxy_range', 'player.roulette_confirm',
    'location_type.emergency_galaxy_fix',
}

# Corvette is officially 輕型巡防艦 in zh-TW (distinct from frigate 巡防艦)
CORVETTE_KEYS = {
    'base.storage_corvette_parts', 'export_config.template_corvette',
    'export_config.template_corvette_snapshot', 'item_category.corvette',
    'item_type.corvette', 'milestone.corvette_parts', 'milestone.dist_any_corvette',
    'milestone.dist_other_corvette', 'milestone.dist_own_corvette',
    'player.state_on_foot_corvette', 'player.state_on_foot_corvette_landed',
    'starship.corvette_no_base', 'starship.corvette_no_seed',
    'starship.corvette_primary_corruption', 'starship.corvette_primary_warning',
    'starship.corvette_warning', 'starship.corvette_warning_title',
    'starship.customisation_corvette_disabled', 'starship.type_corvette',
    'starship.archive_corvette_blocked', 'multiplayer.never_allow_corvette_purchases',
    'multiplayer.allow_save_context_corvette_transfer',
    'multiplayer.allow_only_corvette_ship_purchases',
    'multiplayer.only_corvette_launcher_can_be_repaired',
    'multiplayer.only_corvettes_spawn_when_player_teleports',
}

# Value overrides authored in Simplified; opencc converts to Taiwan script afterwards
KEY_FIX = {
    'starship.type_interceptor': '拦截舰',
    'starship.type_vintage_interceptor': '老式拦截舰',
    'starship.type_explorer': '探索者',
    'starship.type_fighter': '战船',
    'starship.type_shuttle': '太空梭',
    'starship.type_hauler': '拖运船',
    'starship.type_exotic': '外星',
    'item_category.exotic': '外星',
    'outfits.title': '外观：',
    'outfits.slot_number': '外观 {0}',
    'base.worker_armorer': '装甲匠',
    'starship.corvette_warning': '⚠ 存档仅会为“最近登上的护卫舰”保留完整的科技槽位。',
}

# Global term maps (Simplified -> official Taiwan vocabulary). Most specific first.
TERMS = [
    ('多用途工具', '工具组'),
    ('护卫舰', '巡防舰'),
    ('护卫', '巡警'),
    ('异象', '异常'),
    ('符文', '符号'),
    ('远征', '探险'),
    ('星际飞船', '太空船'),
    ('飞船', '太空船'),
    ('定居点', '聚居地'),
    ('套装', '强化套装'),
    ('战团', '中队'),
    ('纳米星团', '奈米机'),
    ('吉克', '吉客族'),
    ('科尔瓦克斯', '科瓦族'),
    ('维吉恩', '维金族'),
    ('配方', '制作方法'),
    ('阿特拉斯', '寰宇'),
    ('战斗机', '战船'),
    ('飞艇', '太空梭'),
    ('自噬体', '自噬'),
    ('装扮', '外观'),
    ('库存', '道具栏'),
    ('空间站', '太空站'),
]

# Taiwan convention prefers corner brackets over curly double quotes
QUOTE_FIX = [('“', '「'), ('”', '」'), ('游戲', '遊戲')]

# Restore Taiwan conventions that the Simplified base does not carry,
# verified against Resources/json/lang/zh-TW.json (the game's own zh-TW pack)
TW_FIX = [
    ('十六進位制', '十六進位'),
    ('十六進制', '十六進位'),
    ('進位制', '進位'),
    ('槽位', '欄位'),
    ('賬戶', '帳戶'),
    ('平臺', '平台'),
    ('程式碼', '代碼'),
    ('重置', '重設'),
    ('更改', '變更'),
    ('選中', '選取'),
    ('界面', '介面'),
    ('隱身塗裝', '潛行塗裝'),
    ('啞光', '霧面'),
    ('當前', '目前'),
    ('常規', '一般'),
    ('單詞', '單字'),
    ('檢測', '偵測'),
    ('定製', '自訂'),
    ('自定義', '自訂'),
    ('型別', '類型'),
    ('空間興趣點', '太空興趣點'),
    ('高階', '進階'),
    ('撤銷', '復原'),
    ('專案', '項目'),
    ('缺失', '缺少'),
    ('在列表中', '在清單中'),
    ('從列表中', '從清單中'),
    ('可執行檔案', '可執行檔'),
    ('執行檔案', '執行檔'),
    ('應用程式', '\ue000APP\ue000'),
    ('應用', '套用'),
    ('\ue000APP\ue000', '應用程式'),
    ('匹配項', '符合項目'),
    ('匹配', '符合'),
    ('疊放', '堆疊'),
    ('點選', '點擊'),
    ('樹形', '樹狀'),
    ('會話', '工作階段'),
    ('本地化', '在地化'),
    ('重啟', '重新啟動'),
    ('雲同步', '雲端同步'),
    ('分組', '群組'),
]


def build_value(k, v):
    v = KEY_FIX.get(k, v)
    if k in CORVETTE_KEYS:
        v = v.replace('护卫舰', '轻型巡防舰')
    if k in GALAXY_KEYS:
        v = v.replace('星系', '银河系')
    for a, b in TERMS:
        v = v.replace(a, b)
    return v


src = json.load(open(SRC, encoding='utf-8'))
cc = opencc.OpenCC('s2twp')
out = {}
for k, v in src.items():
    if k == '_meta.description':
        out[k] = 'NMSE UI字串表 – 繁體中文（潤色版，對齊官方譯名）'
        continue
    v = cc.convert(build_value(k, v))
    for a, b in QUOTE_FIX:
        v = v.replace(a, b)
    for a, b in TW_FIX:
        v = v.replace(a, b)
    out[k] = v

with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
    f.write('\n')

print('wrote', OUT, 'keys', len(out))
