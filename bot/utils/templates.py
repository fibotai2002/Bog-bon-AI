"""
Javob shablonlari (FREE, PRO, BUSINESS) - Lokalizatsiya bilan
"""

from typing import Dict, Any, List
from bot.utils.locales import get_text

def format_free_response(data: Dict[str, Any], lang: str = "uz") -> str:
    """
    FREE tarif uchun javob formatlash
    """
    top_diagnosis = data["diagnoses"][0] if data["diagnoses"] else None
    
    if not top_diagnosis:
        # Xatolik matni locales da "text_advice_error" ga o'xshash yoki yangi
        return get_text("error_processing", lang)
    
    # Headers
    header_prediction = get_text("analysis_header", lang)
    header_confidence = get_text("confidence", lang)
    header_pharmacy = get_text("pharmacy_title", lang)
    header_recipe = get_text("recipe_title", lang)
    header_agro = get_text("agrotechnics", lang)
    header_safety = get_text("safety", lang)
    promo = get_text("pro_promo", lang)
    
    message = f"{header_prediction} {top_diagnosis['name']}\n"
    message += f"{header_confidence} {top_diagnosis['confidence']}%\n\n"
    
    # Treatment
    treatment = top_diagnosis.get("treatment", {})
    
    # Pharmacy request
    if treatment.get("pharmacy_text"):
        message += f"{header_pharmacy}\n<i>\"{treatment['pharmacy_text']}\"</i>\n\n"
    
    # Chemical recipes
    if treatment.get("chemical_recipes"):
        message += f"{header_recipe}\n"
        for chem in treatment["chemical_recipes"]:
            name = chem.get("product_name", "Noma'lum")
            dosage = chem.get("dosage_10l", "")
            method = chem.get("application_method", "")
            
            chem_str = f"• <b>{name}</b>"
            if dosage:
                chem_str += f": {dosage}"
            if method:
                chem_str += f" ({method})"
            message += f"{chem_str}\n"
        message += "\n"

    # Agrotechnics
    if treatment.get("agrotechnics"):
        message += f"{header_agro}\n"
        for agro in treatment["agrotechnics"][:2]:
            message += f"• {agro}\n"
        message += "\n"
    
    # Safety
    safety_note = data.get("safety_note", "")
    if safety_note:
        message += f"{header_safety} {safety_note}\n\n"
    
    message += promo
    
    return message

def format_pro_response(data: Dict[str, Any], lang: str = "uz") -> str:
    """
    PRO tarif uchun javob formatlash
    """
    header_top = get_text("top_diagnosis", lang)
    header_signs = get_text("visual_signs", lang)
    header_pharmacy = get_text("pharmacy_title", lang)
    header_recipe = get_text("recipe_title", lang) # va boshqalar...
    header_bio = get_text("biologic", lang)
    header_agro = get_text("agrotechnics", lang)
    header_severity = get_text("severity", lang)
    header_safety = get_text("safety", lang)

    message = f"{header_top}\n\n"
    
    diagnoses = data["diagnoses"][:2]
    
    for i, diag in enumerate(diagnoses, 1):
        message += f"<b>{i}) {diag['name']}</b> — {diag['confidence']}%\n"
        
        # Vizual belgilar
        if diag.get("why"):
            signs_str = ', '.join(diag['why'][:3])
            message += f"   <i>{header_signs}: {signs_str}</i>\n"
        
        # Treatment
        treatment = diag.get("treatment", {})
        
        # Pharmacy text
        if treatment.get("pharmacy_text"):
            message += f"\n   {header_pharmacy}\n   <i>\"{treatment['pharmacy_text']}\"</i>\n"
        
        # Chemical recipes
        chemicals = treatment.get("chemical_recipes", [])
        if chemicals:
            # 10L ni locales fileda berilgan: "🧴 Retsept (10L suvga):"
            message += f"\n   {header_recipe}\n"
            for chem in chemicals:
                name = chem.get("product_name", "")
                active = chem.get("active_ingredient", "")
                dosage = chem.get("dosage_10l", "")
                method = chem.get("application_method", "")
                frequency = chem.get("frequency", "")
                
                chem_str = f"   • <b>{name}</b>"
                if active:
                    chem_str += f" ({active})"
                chem_str += f": <b>{dosage}</b>"
                if method:
                    chem_str += f" ({method})"
                if frequency:
                    chem_str += f"\n     🔄 {frequency}"
                message += f"{chem_str}\n"

        # Biologic
        bios = treatment.get("biologic_recipes", [])
        if bios:
            message += f"\n   {header_bio}\n"
            for bio in bios:
                message += f"   • {bio}\n"
        
        # Agrotechnics
        agros = treatment.get("agrotechnics", [])
        if agros:
            message += f"\n   {header_agro}\n"
            for agro in agros:
                message += f"   • {agro}\n"
        
        message += "\n" + ("-" * 20) + "\n\n"
    
    # Severity
    severity = data.get("severity", "unknown").upper()
    message += f"{header_severity}: {severity}\n"
    
    # Safety
    safety = data.get("safety_note", "")
    if safety:
        message += f"{header_safety} <i>{safety}</i>"
    
    return message

def format_business_response(data: Dict[str, Any], user_id: int, target_type: str, lang: str = "uz") -> str:
    """
    BUSINESS tarif uchun (Copy-Paste)
    """
    pro_message = format_pro_response(data, lang)
    
    header_copy = get_text("admin_copy", lang)
    
    # Copy paste block
    message = pro_message + "\n\n"
    message += f"{header_copy}\n"
    message += "<code>"
    message += f"[CASE #{user_id}]\n"
    
    # Qismlarni tarjima qilish shart emas bu yerda, admin uchun
    message += f"Qism: {target_type}\n"
    
    crop = data.get("likely_crop", {}).get("name", "Unknown")
    message += f"Ekin: {crop}\n\n"
    
    for i, diag in enumerate(data["diagnoses"][:2], 1):
        message += f"{i}. {diag['name']}\n"
        treatment = diag.get("treatment", {})
        
        if treatment.get("chemical_recipes"):
            message += "   Kimyo:\n"
            for chem in treatment["chemical_recipes"]:
                message += f"   - {chem.get('product_name')}: {chem.get('dosage_10l')}\n"
        
        message += "\n"
        
    message += "</code>"
    return message

def format_admin_channel_message(data: Dict[str, Any], user_id: int, target_type: str) -> str:
    """Admin kanal xabari (o'zgarmaydi)"""
    top_diag = data["diagnoses"][0] if data["diagnoses"] else {}
    name = top_diag.get("name", "Unknown")
    return f"🔔 NEW CASE\nUser: {user_id}\nType: {target_type}\nTop: {name}"

def format_image_quality_error(issues: List[str]) -> str:
    return "⚠️ Rasm sifati past. Tahlil davom etmoqda..."
