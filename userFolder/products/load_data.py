import os
import sys
import django
from django.db import transaction

# --- 1. CONFIGURE DJANGO ENVIRONMENT ---
# Sets up the environment to allow model imports and ORM access
script_dir = os.path.dirname(__file__)
project_root_dir = os.path.abspath(os.path.join(script_dir, '..', '..'))
sys.path.append(project_root_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TuckProject.settings')
django.setup()

# Import the Product model (MUST happen after django.setup())
# NOTE: This assumes Product model now has the three Boolean fields.
from userFolder.products.models import Product 

# =======================================================
# --- ORM FUNCTION FOR MARKING FEATURED PRODUCTS ---
# =======================================================

def mark_offered_products():
    """
    Selects products based on various criteria and updates their boolean flags
    using the correct ORM pattern (ID selection + update) to avoid slicing errors.
    """
    print("\n--- Starting ORM Operation: Marking Offered Products ---")

    try:
        with transaction.atomic():
            
            # 1. Reset all flags (This is fine, no slicing involved)
            Product.objects.all().update(is_featured=False, is_selective=False, is_most_demanded=False)
            print("✅ Reset all flags.")

            # --- 2. Mark 'Featured Items' (e.g., the 5 most recently added products) ---
            # FIX: Get IDs of the sliced products first.
            featured_ids = Product.objects.order_by('-created_at').values_list('id', flat=True)[:5]
            
            # ORM: Use the IDs to filter, then update the subset.
            featured_count = Product.objects.filter(id__in=featured_ids).update(is_featured=True)
            print(f"✅ Marked {featured_count} most recent products as 'is_featured'.")

            # --- 3. Mark 'Selective Items' (e.g., 8 random products) ---
            # FIX: Get IDs of the sliced products first.
            selective_ids = Product.objects.order_by('?').values_list('id', flat=True)[:8]
            
            # ORM: Use the IDs to filter, then update the subset.
            selective_count = Product.objects.filter(id__in=selective_ids).update(is_selective=True)
            print(f"✅ Marked {selective_count} random products as 'is_selective'.")

            # --- 4. Mark 'Most Demanded Items' (e.g., all products priced over $50) ---
            # This query was already correct, as it uses .filter() but no slicing.
            demanded_count = Product.objects.filter(price__gt=50).update(is_most_demanded=True)
            print(f"✅ Marked {demanded_count} products priced over $50.00 as 'is_most_demanded'.")
            
    except Exception as e:
        # Re-raise the exception if it's not the one we fixed, or handle gracefully
        print(f"\n❌ An unrecoverable ORM error occurred (Transaction Rolled Back): {e}")
        return

    # --- Verification ---
    print("\n--- ORM Verification ---")
    # ... (Verification counts remain the same) ...
    print("ORM marking complete.")

# --- The rest of your script remains the same ---
# if __name__ == "__main__":
#     mark_offered_products()
# --- 3. EXECUTE ---
if __name__ == "__main__":
    mark_offered_products()