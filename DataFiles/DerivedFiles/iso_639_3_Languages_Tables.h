// ./DataFiles/DerivedFiles/iso_639_3_Languages_Tables.h
//
// This UTF-8 file was automatically generated by ISO_639_3_Languages.py V0.84 on 2013-08-28 10:30:40.790562
//

#ifndef ISO_639_3_Tables_h
#define ISO_639_3_Tables_h

typedef struct IDDictEntryStruct {
    const unsigned char[3+1] ID;
    const unsigned char* Name;
    const unsigned char Type;
    const unsigned char Scope;
    const unsigned char[2+1] Part1Code;
    const unsigned char[3+1] Part2Code;
} IDDictEntry;

typedef struct NameDictEntryStruct {
    const unsigned char* Name;
    const unsigned char[3+1] ID;
} NameDictEntry;

#endif // ISO_639_3_Tables_h

// end of iso_639_3_Languages_Tables.h