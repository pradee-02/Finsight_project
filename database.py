import os
import json
import datetime
import firebase_admin
from firebase_admin import credentials, firestore

class Database:
    def __init__(self):
        self.is_firebase = False
        self.firestore_db = None
        self.local_db_file = "finsight_local_db.json"
        
        # Try to initialize Firebase
        try:
            # Check if Firebase is already initialized
            if not firebase_admin._apps:
                firebase_admin.initialize_app()
            self.firestore_db = firestore.client()
            
            # Lightweight probe to verify Firestore API is enabled & accessible
            self.firestore_db.collection("users").document("_probe_").get()
            
            self.is_firebase = True
            print("Successfully initialized Firebase Firestore backend!")
        except Exception as e:
            print(f"Firebase Admin SDK initialization failed, API disabled, or no credentials found ({e}).")
            print("Falling back to local JSON file persistence for offline/development mode.")
            self.is_firebase = False
            self._init_local_db()

    def _init_local_db(self):
        if not os.path.exists(self.local_db_file):
            initial_data = {
                "users": {},
                "transactions": [],
                "budgets": [],
                "investments": [],
                "goals": [],
                "accounts": []
            }
            with open(self.local_db_file, "w") as f:
                json.dump(initial_data, f, indent=2)

    def _read_local_db(self):
        try:
            with open(self.local_db_file, "r") as f:
                return json.load(f)
        except Exception:
            self._init_local_db()
            with open(self.local_db_file, "r") as f:
                return json.load(f)

    def _write_local_db(self, data):
        with open(self.local_db_file, "w") as f:
            json.dump(data, f, indent=2)

    # --- USER OPERATIONS ---
    def get_user_by_email(self, email):
        email_lower = email.lower().strip()
        if self.is_firebase:
            try:
                user_ref = self.firestore_db.collection("users").document(email_lower).get()
                if user_ref.exists:
                    return user_ref.to_dict()
            except Exception as e:
                print(f"Firestore get_user error: {e}")
            return None
        else:
            db_data = self._read_local_db()
            return db_data["users"].get(email_lower)

    def create_user(self, user_data):
        email_lower = user_data["email"].lower().strip()
        user_data["email"] = email_lower
        if self.is_firebase:
            try:
                self.firestore_db.collection("users").document(email_lower).set(user_data)
                return True
            except Exception as e:
                print(f"Firestore create_user error: {e}")
                return False
        else:
            db_data = self._read_local_db()
            db_data["users"][email_lower] = user_data
            self._write_local_db(db_data)
            return True

    def update_user(self, email, update_data):
        email_lower = email.lower().strip()
        if self.is_firebase:
            try:
                self.firestore_db.collection("users").document(email_lower).update(update_data)
                return True
            except Exception as e:
                print(f"Firestore update_user error: {e}")
                return False
        else:
            db_data = self._read_local_db()
            if email_lower in db_data["users"]:
                db_data["users"][email_lower].update(update_data)
                self._write_local_db(db_data)
                return True
            return False

    # --- TRANSACTIONS ---
    def get_transactions(self, email):
        email_lower = email.lower().strip()
        if self.is_firebase:
            try:
                docs = self.firestore_db.collection("transactions").where("user_id", "==", email_lower).order_by("date", direction=firestore.Query.DESCENDING).stream()
                return [{**doc.to_dict(), "id": doc.id} for doc in docs]
            except Exception as e:
                # If indexing isn't done yet, fallback to getting all and filtering in memory
                print(f"Firestore query failed, performing in-memory filter: {e}")
                try:
                    docs = self.firestore_db.collection("transactions").where("user_id", "==", email_lower).stream()
                    tx_list = [{**doc.to_dict(), "id": doc.id} for doc in docs]
                    tx_list.sort(key=lambda x: x.get("date", ""), reverse=True)
                    return tx_list
                except Exception as e2:
                    print(f"Firestore fallback transactions get failed: {e2}")
                    return []
        else:
            db_data = self._read_local_db()
            user_txs = [tx for tx in db_data["transactions"] if tx["user_id"] == email_lower]
            user_txs.sort(key=lambda x: x.get("date", ""), reverse=True)
            return user_txs

    def add_transaction(self, tx_data):
        tx_data["user_id"] = tx_data["user_id"].lower().strip()
        tx_data["created_at"] = datetime.datetime.utcnow().isoformat()
        if self.is_firebase:
            try:
                doc_ref = self.firestore_db.collection("transactions").add(tx_data)
                return doc_ref[1].id
            except Exception as e:
                print(f"Firestore add_transaction error: {e}")
                return None
        else:
            db_data = self._read_local_db()
            tx_id = f"tx_{int(datetime.datetime.utcnow().timestamp() * 1000)}"
            tx_data["id"] = tx_id
            db_data["transactions"].append(tx_data)
            self._write_local_db(db_data)
            return tx_id

    def delete_transaction(self, tx_id, email):
        email_lower = email.lower().strip()
        if self.is_firebase:
            try:
                doc_ref = self.firestore_db.collection("transactions").document(tx_id)
                doc = doc_ref.get()
                if doc.exists and doc.to_dict().get("user_id") == email_lower:
                    doc_ref.delete()
                    return True
            except Exception as e:
                print(f"Firestore delete_transaction error: {e}")
            return False
        else:
            db_data = self._read_local_db()
            txs = db_data["transactions"]
            new_txs = [t for t in txs if not (t.get("id") == tx_id and t.get("user_id") == email_lower)]
            if len(txs) != len(new_txs):
                db_data["transactions"] = new_txs
                self._write_local_db(db_data)
                return True
            return False

    # --- BUDGETS ---
    def get_budgets(self, email):
        email_lower = email.lower().strip()
        if self.is_firebase:
            try:
                docs = self.firestore_db.collection("budgets").where("user_id", "==", email_lower).stream()
                return [{**doc.to_dict(), "id": doc.id} for doc in docs]
            except Exception as e:
                print(f"Firestore get_budgets error: {e}")
                return []
        else:
            db_data = self._read_local_db()
            return [b for b in db_data["budgets"] if b["user_id"] == email_lower]

    def set_budget(self, budget_data):
        email_lower = budget_data["user_id"].lower().strip()
        category = budget_data["category"]
        budget_data["user_id"] = email_lower
        budget_data["created_at"] = datetime.datetime.utcnow().isoformat()
        
        if self.is_firebase:
            try:
                # Check if exists
                docs = self.firestore_db.collection("budgets")\
                    .where("user_id", "==", email_lower)\
                    .where("category", "==", category).limit(1).stream()
                existing = list(docs)
                if existing:
                    existing[0].reference.update({"amount": budget_data["amount"]})
                    return existing[0].id
                else:
                    doc_ref = self.firestore_db.collection("budgets").add(budget_data)
                    return doc_ref[1].id
            except Exception as e:
                print(f"Firestore set_budget error: {e}")
                return None
        else:
            db_data = self._read_local_db()
            budgets = db_data["budgets"]
            found = False
            for b in budgets:
                if b["user_id"] == email_lower and b["category"] == category:
                    b["amount"] = budget_data["amount"]
                    found = True
                    break
            if not found:
                budget_data["id"] = f"b_{int(datetime.datetime.utcnow().timestamp() * 1000)}"
                budgets.append(budget_data)
            self._write_local_db(db_data)
            return True

    # --- INVESTMENTS ---
    def get_investments(self, email):
        email_lower = email.lower().strip()
        if self.is_firebase:
            try:
                docs = self.firestore_db.collection("investments").where("user_id", "==", email_lower).stream()
                return [{**doc.to_dict(), "id": doc.id} for doc in docs]
            except Exception as e:
                print(f"Firestore get_investments error: {e}")
                return []
        else:
            db_data = self._read_local_db()
            return [i for i in db_data["investments"] if i["user_id"] == email_lower]

    def add_investment(self, inv_data):
        inv_data["user_id"] = inv_data["user_id"].lower().strip()
        inv_data["created_at"] = datetime.datetime.utcnow().isoformat()
        if self.is_firebase:
            try:
                doc_ref = self.firestore_db.collection("investments").add(inv_data)
                return doc_ref[1].id
            except Exception as e:
                print(f"Firestore add_investment error: {e}")
                return None
        else:
            db_data = self._read_local_db()
            inv_id = f"inv_{int(datetime.datetime.utcnow().timestamp() * 1000)}"
            inv_data["id"] = inv_id
            db_data["investments"].append(inv_data)
            self._write_local_db(db_data)
            return inv_id

    def delete_investment(self, inv_id, email):
        email_lower = email.lower().strip()
        if self.is_firebase:
            try:
                doc_ref = self.firestore_db.collection("investments").document(inv_id)
                doc = doc_ref.get()
                if doc.exists and doc.to_dict().get("user_id") == email_lower:
                    doc_ref.delete()
                    return True
            except Exception as e:
                print(f"Firestore delete_investment error: {e}")
            return False
        else:
            db_data = self._read_local_db()
            invs = db_data["investments"]
            new_invs = [i for i in invs if not (i.get("id") == inv_id and i.get("user_id") == email_lower)]
            if len(invs) != len(new_invs):
                db_data["investments"] = new_invs
                self._write_local_db(db_data)
                return True
            return False

    # --- GOALS ---
    def get_goals(self, email):
        email_lower = email.lower().strip()
        if self.is_firebase:
            try:
                docs = self.firestore_db.collection("goals").where("user_id", "==", email_lower).stream()
                return [{**doc.to_dict(), "id": doc.id} for doc in docs]
            except Exception as e:
                print(f"Firestore get_goals error: {e}")
                return []
        else:
            db_data = self._read_local_db()
            return [g for g in db_data["goals"] if g["user_id"] == email_lower]

    def add_goal(self, goal_data):
        goal_data["user_id"] = goal_data["user_id"].lower().strip()
        goal_data["created_at"] = datetime.datetime.utcnow().isoformat()
        if self.is_firebase:
            try:
                doc_ref = self.firestore_db.collection("goals").add(goal_data)
                return doc_ref[1].id
            except Exception as e:
                print(f"Firestore add_goal error: {e}")
                return None
        else:
            db_data = self._read_local_db()
            goal_id = f"g_{int(datetime.datetime.utcnow().timestamp() * 1000)}"
            goal_data["id"] = goal_id
            db_data["goals"].append(goal_data)
            self._write_local_db(db_data)
            return goal_id

    def update_goal_progress(self, goal_id, added_amount, email):
        email_lower = email.lower().strip()
        if self.is_firebase:
            try:
                doc_ref = self.firestore_db.collection("goals").document(goal_id)
                doc = doc_ref.get()
                if doc.exists and doc.to_dict().get("user_id") == email_lower:
                    data = doc.to_dict()
                    new_amount = float(data.get("currentAmount", 0)) + float(added_amount)
                    status = "Completed" if new_amount >= float(data.get("targetAmount", 0)) else "In Progress"
                    doc_ref.update({
                        "currentAmount": new_amount,
                        "status": status
                    })
                    return True
            except Exception as e:
                print(f"Firestore update_goal error: {e}")
            return False
        else:
            db_data = self._read_local_db()
            goals = db_data["goals"]
            for g in goals:
                if g.get("id") == goal_id and g.get("user_id") == email_lower:
                    new_amount = float(g.get("currentAmount", 0)) + float(added_amount)
                    g["currentAmount"] = new_amount
                    g["status"] = "Completed" if new_amount >= float(g.get("targetAmount", 0)) else "In Progress"
                    self._write_local_db(db_data)
                    return True
            return False

    def delete_goal(self, goal_id, email):
        email_lower = email.lower().strip()
        if self.is_firebase:
            try:
                doc_ref = self.firestore_db.collection("goals").document(goal_id)
                doc = doc_ref.get()
                if doc.exists and doc.to_dict().get("user_id") == email_lower:
                    doc_ref.delete()
                    return True
            except Exception as e:
                print(f"Firestore delete_goal error: {e}")
            return False
        else:
            db_data = self._read_local_db()
            goals = db_data["goals"]
            new_goals = [g for g in goals if not (g.get("id") == goal_id and g.get("user_id") == email_lower)]
            if len(goals) != len(new_goals):
                db_data["goals"] = new_goals
                self._write_local_db(db_data)
                return True
            return False

    # --- ACCOUNTS ---
    def get_accounts(self, email):
        email_lower = email.lower().strip()
        if self.is_firebase:
            try:
                docs = self.firestore_db.collection("accounts").where("user_id", "==", email_lower).stream()
                return [{**doc.to_dict(), "id": doc.id} for doc in docs]
            except Exception as e:
                print(f"Firestore get_accounts error: {e}")
                return []
        else:
            db_data = self._read_local_db()
            return [a for a in db_data["accounts"] if a["user_id"] == email_lower]

    def add_account(self, acc_data):
        acc_data["user_id"] = acc_data["user_id"].lower().strip()
        acc_data["created_at"] = datetime.datetime.utcnow().isoformat()
        if self.is_firebase:
            try:
                doc_ref = self.firestore_db.collection("accounts").add(acc_data)
                return doc_ref[1].id
            except Exception as e:
                print(f"Firestore add_account error: {e}")
                return None
        else:
            db_data = self._read_local_db()
            acc_id = f"acc_{int(datetime.datetime.utcnow().timestamp() * 1000)}"
            acc_data["id"] = acc_id
            db_data["accounts"].append(acc_data)
            self._write_local_db(db_data)
            return acc_id

# Instantiate shared DB engine
db_engine = Database()
