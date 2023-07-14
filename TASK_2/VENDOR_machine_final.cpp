#include <iostream>
#include <unordered_map>

using namespace std;

enum class State {  //declaring the states
    IDLE,
    CHOOSE_DRINK,
    COLLECT_COINS,
    OUT,
    REFILL,
    CANCEL
};

class VendingMachine {   //creating a class representing Vending Machine
public:
    VendingMachine() : currentState(State::IDLE), selectedDrink(""), insertedAmount(0), totalCount(400) {}

    void run() {
        while (true) {
            displayCurrentState();
            handleState(currentState);
        }
    }

private:
    State currentState;
    string selectedDrink;
    int insertedAmount;
    int totalCount;
    unordered_map<string, int> drinkStocks = {
        {"PEPS", 50},
        {"MDEW", 50},
        {"DPEP", 50},
        {"COKE", 50},
        {"GATO", 50},
        {"DCOK", 50},
        {"MINM", 50},
        {"TROP", 50}
    };
    unordered_map<string, int> drinkCosts = {
        {"PEPS", 30},
        {"MDEW", 30},
        {"DPEP", 50},
        {"COKE", 20},
        {"GATO", 20},
        {"DCOK", 30},
        {"MINM", 25},
        {"TROP", 30}
    };

    void displayCurrentState() {   // this function displays the current State of the machine
        cout<< "----------------------\n";
        cout << "Current State: ";
        switch (currentState) {
            case State::IDLE:
                cout << "IDLE\n";
                cout << "----------------------\n";
                displayDrinkMenu();
                break;
            case State::CHOOSE_DRINK:
                cout << "CHOOSE_DRINK\n";
                cout << "----------------------\n";
                break;
            case State::COLLECT_COINS:
                cout << "COLLECT_COINS\n";
                cout << "----------------------\n";
                break;
            case State::OUT:
                cout << "OUT\n";
                cout << "----------------------\n";
                break;
        }
        
    }

    void displayDrinkMenu() {
        cout << "Drink Menu:\n";
        cout << "1. Pepsi (PEPS) - Cost: 30 , Quantity: "<<drinkStocks["PEPS"]<<endl;
        cout << "2. Mountain Dew (MDEW) - Cost: 30 , Quantity: "<<drinkStocks["MDEW"]<<endl;
        cout << "3. Dr. Pepper (DPEP) - Cost: 50 , Quantity: "<<drinkStocks["DPEP"]<<endl;
        cout << "4. Coke (COKE) - Cost: 20 , Quantity: "<<drinkStocks["COKE"]<<endl;
        cout << "5. Gatorade (GATO) - Cost: 20 , Quantity: "<<drinkStocks["GATO"]<<endl;
        cout << "6. Diet Coke (DCOK) - Cost: 30 , Quantity: "<<drinkStocks["DCOK"]<<endl;
        cout << "7. Minute Maid (MINM) - Cost: 25 , Quantity: "<<drinkStocks["MINM"]<<endl;
        cout << "8. Tropicana (TROP) - Cost: 30 , Quantity: "<<drinkStocks["TROP"]<<endl;
        cout << "----------------------\n";
    }

    void handleState(State state) {
        switch (state) {
            case State::IDLE:
                idle_state();
                break;
            case State::CHOOSE_DRINK:
                select_drink();
                break;
            case State::COLLECT_COINS:
                collect_coins();
                break;
            case State::OUT:
                give_drink();
                break;
            case State::REFILL:
                refill();
                break;
            case State::CANCEL:
                cancel();
                break;
        }
    }

    string take_input(){
        string input="";
        cin>>input;
        return input;
    }
    //-------------------------------
    void idle_state(){
        if(totalCount<=0){
            cout<<"NO MORE DRINKS LEFT\nTo refill the machine\nType: REFILL\n";
            string input= take_input();
            if(input=="REFILL")
                currentState=State::REFILL;
            return;
        }
        cout<<"To buy a drink type: BUY"<<endl;
        string input= take_input();
        if(input=="BUY"){
            currentState= State::CHOOSE_DRINK;
        }
        else{
            cout<<"Invalid input !!!"<<endl;
        }
    }
    //-------------------------------
    int search_drink(string code){
        string drink[]={"PEPS","MDEW","DPEP","COKE","GATO","DCOK","MINM","TROP"};

        for(int i=0;i<8;i++){
            if(drink[i]== (code)){
                if( drinkStocks[code]>0)return 1;
                else return 0;
            } 
        }
        return -1;
    }

    void select_drink(){
        cout<<"To cancel type: CANCEL"<<endl;
        cout<<"Enter the code for the drink:"<<endl;
        string code = take_input();

        if(code=="CANCEL"){
            currentState=State::CANCEL;
            return;
        }

        if(search_drink(code)==1){
        selectedDrink=code;
        currentState=State::COLLECT_COINS;
        }
        else if(search_drink(code)==0){
            cout<<"The drink is out of stock. Please select another drink !!!"<<endl;
        }
        else{
            cout<<"Invalid input !!!"<<endl;
        }
    }
    //-------------------------------
    void collect_coins(){
        int amount;
        cout<<"To cancel enter -1"<<endl;
        cout<<"Enter the amount to pay: "<<endl;
        cin>>amount;
        if(amount==-1){
            currentState=State::CANCEL;
            return;
        }
        if(amount>=drinkCosts[selectedDrink]){
            insertedAmount=amount;
            currentState=State::OUT;
        }
        else{
            cout<<"The amount entered is less than the required amount."<<endl;
            cout<<"The required amount for drink "<<selectedDrink<<" is: "<<drinkCosts[selectedDrink]<<endl;
        }
    }
    //-------------------------------
    void give_drink(){
        drinkStocks[selectedDrink]--;
        totalCount--;
        cout<<"Please collect the drink: "<<selectedDrink<<endl;
        if(insertedAmount>drinkCosts[selectedDrink]){
            cout<<"Collect the change of: "<<insertedAmount-drinkCosts[selectedDrink]<<endl;
        }
        cout<<"Transaction completed !!!"<<endl;
        insertedAmount=0;
        selectedDrink="";
        currentState= State::IDLE;
    }
    //-------------------------------
    void refill(){
        for (auto& pair : drinkStocks) {
            pair.second = 50;
        }
        totalCount=400;
        cout << "Stocks refilled.\n";
        currentState = State::IDLE;
    }
    //-------------------------------
    void cancel(){ // cancelling the process
        cout<< "Cancelling\n";
        currentState= State::IDLE;
    }
    //-------------------------------
    
};

int main() {
    VendingMachine vendingMachine;
    vendingMachine.run();
    return 0;
}
