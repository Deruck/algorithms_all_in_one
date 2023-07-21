#include <unordered_map>

struct Node {
public:
    int key;
    int val;
    Node* pre = nullptr;
    Node* next = nullptr;

    Node(int key, int val): key(key), val(val) {}

    static void link(Node* pre, Node* next) {
        if (pre != nullptr) {
            pre->next = next;
        }
        if (next != nullptr) {
            next->pre = pre;
        }
    }
};

class LRUCache {
public:
    /*
    以 正整数 作为容量 capacity 初始化 LRU 缓存*/
    LRUCache(int capacity): capacity_(capacity) {
        head_ = new Node(-1, -1);
        tail_ = new Node(-1, -1);
        Node::link(head_, tail_);
    }

    /*
    如果关键字 key 存在于缓存中，则返回关键字的值，否则返回 -1。O(1) 时间复杂度。
    */
    int get(int key) {
        int res = -1;
        if (auto iter = node_map_.find(key); iter != node_map_.end()){
            res = iter->second->val;
            move_to_head(iter->second);
        }
        return res;
    }

    /*
    如果关键字 key 已经存在，则变更其数据值 value ；如果不存在，则向缓存中插入该组 key-value 。
    如果插入操作导致关键字数量超过 capacity ，则应该 逐出 最久未使用的关键字。O(1) 时间复杂度。
    */
    void put(int key, int value) {
        if (auto iter = node_map_.find(key); iter != node_map_.end()) {
            iter->second->val = value;
            move_to_head(iter->second);
        }
        else {
            auto *node = new Node(key, value);
            node_map_.insert({key, node});
            move_to_head(node);
            if (size_ < capacity_) {
                size_++;
            } else {
                remove_tail();
            }
        }
    }

private:
    std::unordered_map<int, Node *> node_map_;
    int capacity_ = 0;
    int size_ = 0;
    Node *head_;
    Node *tail_;

private:
    void move_to_head(Node *node) {
        if (node->pre != nullptr && node->next != nullptr) {
            Node::link(node->pre, node->next);
        }
        Node::link(node, head_->next);
        Node::link(head_, node);
    }

    void remove_tail() {
        auto *node = tail_->pre;
        if (node == head_) {
            return;
        }
        Node::link(node->pre, tail_);
        node_map_.erase(node->key);
        delete node;
    }
};